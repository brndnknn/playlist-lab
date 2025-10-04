"""Test doubles for simulating rate-limit and transient failures."""

from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any, List, Sequence

import requests


def make_openai_success(text: str = "stub", usage: Any | None = None) -> SimpleNamespace:
    return SimpleNamespace(output_text=text, usage=usage or {})


class FakeRateLimitError(Exception):
    """Mimics common OpenAI rate-limit errors with optional headers."""

    def __init__(
        self,
        message: str = "Rate limit hit",
        *,
        status: int = 429,
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status
        self.response = SimpleNamespace(headers=headers or {})


class FakeServerError(Exception):
    def __init__(self, status: int = 500, message: str = "Server error") -> None:
        super().__init__(message)
        self.status_code = status
        self.response = SimpleNamespace(headers={})


class FakeAsyncOpenAIClient:
    """AsyncOpenAI shim that replays a scripted sequence of outcomes."""

    def __init__(self, sequence: Sequence[Any]) -> None:
        self.responses = _FakeResponses(sequence)


class _FakeResponses:
    def __init__(self, sequence: Sequence[Any]) -> None:
        self._queue: List[Any] = list(sequence)

    async def create(self, **_: Any) -> Any:
        if not self._queue:
            raise AssertionError("FakeResponses exhausted")
        action = self._queue.pop(0)
        if isinstance(action, Exception):
            raise action
        return action


@dataclass
class FakeRequestsResponse:
    status_code: int
    text: str = ""
    headers: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        self.headers = self.headers or {}

    def raise_for_status(self) -> None:
        if 400 <= self.status_code:
            raise requests.exceptions.HTTPError(
                f"HTTP {self.status_code}", response=self
            )
