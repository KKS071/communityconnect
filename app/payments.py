"""S-6 AC-19 first monthly charge and AC-20 Pending replay.

AC-21 manual payment and AC-22 failed retry are separate tasks.
Only a single runner is supported (D32); no live processor integration.
"""
from dataclasses import dataclass
from datetime import date

from app import clock, db, processor


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
                    idempotency_key: str) -> str | None:
    """Charge using persisted values; leave Pending if unavailable or interrupted."""
    try:
        result = processor.get_processor().charge(token, amount_cents, idempotency_key)
    except processor.ProcessorUnavailable:
        return None
    if result.status not in ("succeeded", "declined"):
        raise ValueError(f"Unexpected processor result: {result.status!r}")
    status = "Paid" if result.status == "succeeded" else "Failed"
    db.finish_payment(payment_id, status, result.processor_id)
    return status


def run_due_payments(today: date) -> RunResult:
    """Replay Pending attempts from any month before processing current due schedules."""
    month = today.strftime("%Y-%m")
    charged = failed = skipped = 0

    # D26: recover persisted attempts first, reusing the original key and amount.
    for p in db.pending_payments():
        if db.has_paid_payment(p["unit_id"], p["billing_month"]):
            continue
        if p["method"] == "ach":
            continue  # ACH settlement remains OQ2.
        status = _charge_pending(p["id"], p["token"], p["amount_cents"],
                                 p["idempotency_key"])
        if status == "Paid":
            charged += 1
        elif status == "Failed":
            failed += 1
        else:
            skipped += 1

    for s in db.due_schedules():
        scheduled_day = date(today.year, today.month, s["day_of_month"])
        created_day = date.fromisoformat(s["created_at"][:10])
        if today < scheduled_day or scheduled_day <= created_day:
            continue
        if s["method"] == "ach":
            continue  # ACH settlement remains OQ2.
        prior = db.latest_payment(s["unit_id"], month)
        if prior is not None:
            if prior["status"] == "Paid":
                skipped += 1
            # Pending already replayed; Failed retries are AC-22.
            continue
        key = f'{s["unit_id"]}:{month}:1'
        payment_id = db.create_pending_payment(
            s["unit_id"], month, s["dues_amount_cents"], s["method"], key,
            _timestamp(),
        )  # Committed before the processor call (D4/D31).
        status = _charge_pending(payment_id, s["token"],
                                 s["dues_amount_cents"], key)
        if status == "Paid":
            charged += 1
        elif status == "Failed":
            failed += 1
        else:
            skipped += 1
    return RunResult(charged=charged, failed=failed, skipped=skipped)


def record_manual_payment(unit_id: int, billing_month: str):
    """AC-21 is not implemented yet."""
    raise NotImplementedError("Manual payments are reserved for AC-21")
