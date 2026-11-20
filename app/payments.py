"""AC-19: create and charge a monthly scheduled payment once (S-6 D4, D25).

AC-20 Pending replay, AC-21 manual payments and AC-22 retries are separate tasks.
One runner at a time only (D32); no live processor integration.
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


def run_due_payments(today: date) -> RunResult:
    """Run first-attempt charges for active, due debit/credit schedules.

    A Pending row is committed before each processor call; an unavailable processor
    leaves it Pending. Later ACs will implement Pending replay and Failed retries.
    """
    month = today.strftime("%Y-%m")
    charged = failed = skipped = 0
    schedules = db.due_schedules()
    for s in schedules:
        scheduled_day = date(today.year, today.month, s["day_of_month"])
        created_day = date.fromisoformat(s["created_at"][:10])
        if today < scheduled_day or scheduled_day <= created_day:
            continue
        # ACH settlement is OQ2; do not assign Paid semantics to ACH.
        if s["method"] == "ach":
            continue
        prior = db.latest_payment(s["unit_id"], month)
        if prior is not None:
            if prior["status"] == "Paid":
                skipped += 1
            # Pending replay is AC-20; Failed retry is AC-22.
            continue
        key = f'{s["unit_id"]}:{month}:1'
        payment_id = db.create_pending_payment(
            s["unit_id"], month, s["dues_amount_cents"], s["method"], key, _timestamp()
        )
        # The INSERT transaction is committed before calling the processor (D4/D31).
        try:
            result = processor.get_processor().charge(s["token"], s["dues_amount_cents"], key)
        except processor.ProcessorUnavailable:
            skipped += 1
            continue
        if result.status not in ("succeeded", "declined"):
            raise ValueError(f"Unexpected processor result: {result.status!r}")
        status = "Paid" if result.status == "succeeded" else "Failed"
        db.finish_payment(payment_id, status, result.processor_id)
        if status == "Paid":
            charged += 1
        else:
            failed += 1
    return RunResult(charged=charged, failed=failed, skipped=skipped)


def record_manual_payment(unit_id: int, billing_month: str):
    """AC-21 is not implemented yet; never silently record a manual payment."""
    raise NotImplementedError("Manual payments are reserved for AC-21")
