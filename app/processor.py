"""S-6 processor abstraction and deterministic test fake (D28-D29).

Real Stripe integration is deliberately deferred to a separately approved task.
"""
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ChargeResult:
    status: str  # 'succeeded' or 'declined'
    processor_id: str


class ProcessorUnavailable(Exception):
    """No confirmed processor result; leave payment Pending."""


class Processor(Protocol):
    def charge(self, token: str, amount_cents: int, idempotency_key: str) -> ChargeResult: ...


class FakeProcessor:
    def __init__(self, declined_tokens: frozenset[str] = frozenset(),
                 unavailable: bool = False):
        self.declined_tokens = declined_tokens
        self.unavailable = unavailable
        self.calls: list[tuple[str, int, str]] = []
        self._results: dict[str, ChargeResult] = {}

    def charge(self, token: str, amount_cents: int, idempotency_key: str) -> ChargeResult:
        self.calls.append((token, amount_cents, idempotency_key))
        if idempotency_key in self._results:
            return self._results[idempotency_key]
        if self.unavailable:
            raise ProcessorUnavailable("Fake processor unavailable")
        status = "declined" if token in self.declined_tokens else "succeeded"
        result = ChargeResult(status, f"fake_{len(self._results) + 1}")
        self._results[idempotency_key] = result
        return result


class StripeTestProcessor:
    """Placeholder; Stripe integration needs separate dependency and task approval."""
    def charge(self, token: str, amount_cents: int, idempotency_key: str) -> ChargeResult:
        raise ProcessorUnavailable("Stripe test integration is not implemented")


_processor: Processor = StripeTestProcessor()


def get_processor() -> Processor:
    return _processor


def set_processor(p: Processor) -> None:
    global _processor
    _processor = p
