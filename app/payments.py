"""S-6 scheduled dues: AC-19 first charge, AC-20 Pending replay, AC-21 manual payment and
AC-22 retry of a declined attempt (D17, D35).

Only a single runner is supported (D32); no live processor integration.
"""
from dataclasses import dataclass
from datetime import date
import re

from app import clock, db, processor, settings


@dataclass(frozen=True)
class RunResult:
    charged: int = 0
    failed: int = 0
    skipped: int = 0


class AlreadyPaid(Exception):
    pass


class PaymentPending(Exception):
    pass


def _timestamp() -> str:
    return clock.now().strftime("%Y-%m-%dT%H:%M:%SZ")


def _charge_pending(payment_id: int, token: str, amount_cents: int,
                    idempotency_key: str, today: date) -> str | None:
    """Charge using persisted values; leave Pending if unavailable or interrupted.

    A declined charge stores today as failed_on (D17). Return 'Paid' or 'Failed', None if
    the payment stays Pending, or 'Unchanged' if it was already completed with the same
    result (AGENT-03 F-11; D16: not counted again). If it was completed with a different
    result, raise RuntimeError so the run stops without overwriting it (D31).
    """
    try:
        result = processor.get_processor().charge(token, amount_cents, idempotency_key)
    except processor.ProcessorUnavailable:
        return None
    if result.status not in ("succeeded", "declined"):
        raise ValueError(f"Unexpected processor result: {result.status!r}")
    status = "Paid" if result.status == "succeeded" else "Failed"
    if db.finish_payment(payment_id, status, result.processor_id, today.isoformat()):
        return status
    stored = db.payment_status(payment_id)
    if stored != status:
        raise RuntimeError(f"Payment {payment_id} is stored as {stored!r} but the processor "
                           f"reported {status!r}; stopping the run (AGENT-03 F-11, D31)")
    return "Unchanged"  # already completed with this result; not counted again (F-11, D16)


def run_due_payments(today: date) -> RunResult:
    """Replay Pending attempts from any month, then process current due schedules."""
    month = today.strftime("%Y-%m")
    charged = failed = skipped = 0

    # D26: recover persisted attempts first, reusing the original key, amount and attempt.
    for p in db.pending_payments():
        if db.has_paid_payment(p["unit_id"], p["billing_month"]):
            continue
        if p["method"] == "ach":
            continue  # ACH settlement remains OQ2.
        status = _charge_pending(p["id"], p["token"], p["amount_cents"],
                                 p["idempotency_key"], today)
        if status == "Paid":
            charged += 1
        elif status == "Failed":
            failed += 1
        elif status is None:
            skipped += 1

    for s in db.due_schedules():
        scheduled_day = date(today.year, today.month, s["day_of_month"])
        created_day = date.fromisoformat(s["created_at"][:10])
        if today < scheduled_day or scheduled_day <= created_day:
            continue
        if s["method"] == "ach":
            continue  # ACH settlement remains OQ2.
        if db.has_paid_payment(s["unit_id"], month):
            skipped += 1  # D25: the month is Paid (R1, R3); AGENT-03 F-02.
            continue
        prior = db.latest_payment(s["unit_id"], month)
        if prior is None:
            attempt = 1
        elif (prior["status"] == "Failed"
              and prior["attempt"] < settings.MAX_PAYMENT_ATTEMPTS):
            attempt = prior["attempt"] + 1  # D17 retry; the delay is checked under the lock
        else:
            # D25: a Pending left after the D26 replay gets no new attempt; D17: after the
            # last allowed attempt fails, nothing more happens this month.
            continue
        key = f'{s["unit_id"]}:{month}:{attempt}'
        payment_id, conflict = db.claim_pending_payment(
            s["unit_id"], month, s["dues_amount_cents"], s["method"], key, _timestamp(),
            attempt=attempt, today=today, retry_delay_days=settings.RETRY_DELAY_DAYS,
            max_attempts=settings.MAX_PAYMENT_ATTEMPTS,
        )  # Re-checked under the unit lock; committed before the charge (D4/D31; F-01).
        if conflict == "Paid":
            skipped += 1  # a manual payment committed first (D25, D27; F-01)
            continue
        if conflict is not None:
            continue  # another payment appeared, or the retry is not due yet (D17, D25)
        status = _charge_pending(payment_id, s["token"],
                                 s["dues_amount_cents"], key, today)
        if status == "Paid":
            charged += 1
        elif status == "Failed":
            failed += 1
        elif status is None:
            skipped += 1
    return RunResult(charged=charged, failed=failed, skipped=skipped)


def record_manual_payment(unit_id: int, billing_month: str) -> dict:
    """Record an already-received manual payment, without processor charging.

    A Paid or Pending payment prevents insertion; Failed attempts do not (D27).
    """
    if (not isinstance(billing_month, str)
            or re.fullmatch(r"[0-9]{4}-(0[1-9]|1[0-2])", billing_month) is None):
        raise ValueError("Invalid billing month")
    if type(unit_id) is not int or unit_id <= 0:
        raise ValueError("Unknown unit")
    row, conflict = db.create_manual_payment(unit_id, billing_month, _timestamp())
    if conflict == "Paid":
        raise AlreadyPaid("Payment already recorded for this month")
    if conflict == "Pending":
        raise PaymentPending("A scheduled payment is still Pending")
    return row
