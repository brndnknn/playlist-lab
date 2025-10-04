import asyncio

import pytest
import requests

from playlist_generation import openai_async_manager as oam
from playlist_generation.openai_async_manager import OpenAIAsyncManager
from utils import helpers

from .mocks import (
    FakeAsyncOpenAIClient,
    FakeRateLimitError,
    FakeServerError,
    FakeRequestsResponse,
    FakeInvalidPromptError,
    make_openai_success,
)


def test_openai_manager_respects_retry_after_header(monkeypatch):
    delays: list[float] = []

    async def fake_sleep(duration: float) -> None:
        delays.append(duration)

    client = FakeAsyncOpenAIClient(
        [
            FakeRateLimitError(headers={"Retry-After": "0.10"}),
            make_openai_success("ok", {"total_tokens": 3}),
        ]
    )
    manager = OpenAIAsyncManager(
        api_key="test-key",
        max_retries=4,
        backoff_base=0.2,
        client=client,
        sleep=fake_sleep,
    )

    text, usage = asyncio.run(manager.get_response("prompt"))

    assert text == "ok"
    assert usage == {"total_tokens": 3}
    assert pytest.approx(delays) == [0.10]


def test_openai_manager_exponential_backoff(monkeypatch):
    delays: list[float] = []

    async def fake_sleep(duration: float) -> None:
        delays.append(duration)

    monkeypatch.setattr(oam.random, "uniform", lambda *_: 0.0)

    client = FakeAsyncOpenAIClient(
        [
            FakeServerError(status=500),
            FakeServerError(status=503),
            make_openai_success("done"),
        ]
    )
    manager = OpenAIAsyncManager(
        api_key="key",
        max_retries=5,
        backoff_base=0.05,
        client=client,
        sleep=fake_sleep,
    )

    text, _ = asyncio.run(manager.get_response("prompt"))

    assert text == "done"
    assert pytest.approx(delays) == [0.05, 0.10]


def test_openai_manager_does_not_retry_on_client_error():
    client = FakeAsyncOpenAIClient([FakeServerError(status=400, message="Bad request")])
    manager = OpenAIAsyncManager(api_key="key", max_retries=3, client=client)

    with pytest.raises(FakeServerError):
        asyncio.run(manager.get_response("prompt"))


def test_openai_manager_raises_after_retry_exhaustion(monkeypatch):
    delays: list[float] = []

    async def fake_sleep(duration: float) -> None:
        delays.append(duration)

    monkeypatch.setattr(oam.random, "uniform", lambda *_: 0.0)

    client = FakeAsyncOpenAIClient(
        [FakeServerError(status=502) for _ in range(5)]
    )
    manager = OpenAIAsyncManager(
        api_key="key",
        max_retries=3,
        backoff_base=0.1,
        client=client,
        sleep=fake_sleep,
    )

    with pytest.raises(FakeServerError):
        asyncio.run(manager.get_response("prompt"))

    assert pytest.approx(delays) == [0.1, 0.2]


def test_openai_manager_retries_invalid_prompt(monkeypatch):
    delays: list[float] = []

    async def fake_sleep(duration: float) -> None:
        delays.append(duration)

    monkeypatch.setattr(oam.random, "uniform", lambda *_: 0.0)

    client = FakeAsyncOpenAIClient(
        [
            FakeInvalidPromptError(
                message="Invalid prompt: flagged by policy", code="invalid_prompt"
            ),
            make_openai_success("clean")
        ]
    )

    manager = OpenAIAsyncManager(
        api_key="key",
        max_retries=3,
        backoff_base=0.2,
        client=client,
        sleep=fake_sleep,
    )

    text, _ = asyncio.run(manager.get_response("prompt"))

    assert text == "clean"
    assert pytest.approx(delays) == [0.2]


def test_logged_request_retries_on_rate_limit(monkeypatch):
    delays: list[float] = []

    def fake_sleep(duration: float) -> None:
        delays.append(duration)

    monkeypatch.setattr(helpers.random, "uniform", lambda *_: 0.0)
    monkeypatch.setattr(helpers.time, "sleep", fake_sleep)

    sequence = [
        FakeRequestsResponse(429, text="busy", headers={"Retry-After": "0.25"}),
        FakeRequestsResponse(200, text="ok"),
    ]
    call_count = {"idx": 0}

    def fake_request(method, url, **kwargs):
        idx = call_count["idx"]
        call_count["idx"] += 1
        response = sequence[idx]
        if isinstance(response, Exception):
            raise response
        return response

    monkeypatch.setattr(helpers.requests, "request", fake_request)

    resp = helpers.logged_request("get", "https://example.com/api", retries=3)

    assert resp.status_code == 200
    assert pytest.approx(delays) == [0.25]
    assert call_count["idx"] == 2


def test_logged_request_retries_on_timeout(monkeypatch):
    delays: list[float] = []

    def fake_sleep(duration: float) -> None:
        delays.append(duration)

    monkeypatch.setattr(helpers.random, "uniform", lambda *_: 0.0)
    monkeypatch.setattr(helpers.time, "sleep", fake_sleep)

    sequence = [
        requests.exceptions.Timeout("timeout"),
        FakeRequestsResponse(200, text="ok"),
    ]
    call_count = {"idx": 0}

    def fake_request(method, url, **kwargs):
        idx = call_count["idx"]
        call_count["idx"] += 1
        action = sequence[idx]
        if isinstance(action, Exception):
            raise action
        return action

    monkeypatch.setattr(helpers.requests, "request", fake_request)

    resp = helpers.logged_request("post", "https://example.com/resource", timeout=1)

    assert resp.status_code == 200
    assert pytest.approx(delays) == [0.5]
    assert call_count["idx"] == 2


def test_logged_request_raises_after_exhausting_retries(monkeypatch):
    delays: list[float] = []

    def fake_sleep(duration: float) -> None:
        delays.append(duration)

    monkeypatch.setattr(helpers.random, "uniform", lambda *_: 0.0)
    monkeypatch.setattr(helpers.time, "sleep", fake_sleep)

    sequence = [FakeRequestsResponse(503, text="down")] * 4
    call_count = {"idx": 0}

    def fake_request(method, url, **kwargs):
        idx = call_count["idx"]
        call_count["idx"] += 1
        return sequence[idx]

    monkeypatch.setattr(helpers.requests, "request", fake_request)

    with pytest.raises(requests.exceptions.HTTPError):
        helpers.logged_request("get", "https://example.com", retries=2, backoff_base=0.05)

    assert pytest.approx(delays) == [0.05, 0.1]
    assert call_count["idx"] == 3
