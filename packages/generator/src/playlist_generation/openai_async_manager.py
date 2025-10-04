from typing import Optional, Tuple, Callable, Awaitable, TypeVar
import asyncio
import random
import time
from openai import AsyncOpenAI

R = TypeVar("R")

class OpenAIAsyncManager:
    """
    Async twin of OpenAIManger. Same inputs/outputs, but awaitable.
    """
    def __init__(
            self,
            api_key: str,
            model: str = "gpt-5-nano",
            max_retries: int = 5,
            backoff_base: float = 0.5,
            client: Optional[AsyncOpenAI] = None,
            sleep: Optional[Callable[[float], Awaitable[None]]] = None,
    ):
        self.model = model
        self.client = client or AsyncOpenAI(api_key=api_key)
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self._sleep = sleep or asyncio.sleep
        self.system_prompt = (
            """You are an AI DJ with a mischievous sense of humor and impeccable taste in music.
                Your job is to create playlists in response to surreal, whimsical, or unusual prompts.

                Rules:

                Output 20–30 songs, one per line, in the format:
                Song Title — Artist

                Only include real, verifiable songs (no invented titles or fake artists).

                Do not include more than two songs by the same artist.

                Keep the playlist coherent — it should feel intentional and unified.

                Infuse the playlist with quirky, funny, punny, and creative choices that cleverly reference the prompt.

                Balance thematic alignment (lyrics, titles, or artist names connected to the prompt) with musical flow (songs that could believably exist together in one playlist).

                Do not include explanations, commentary, numbering, or extra prose. Output only the playlist text.


                Goal:
                Make the playlist surprising, witty, and cohesive — something that feels like a joke, a story, and a genuinely listenable set of songs all at once.
                """
        )
        self.alt_sys_prompt = (
                "Convert the given playlist of songs into a list in JSON format. "
                "Each item should be an object with keys 'title' and 'artist'. "
                "Only include songs contained in the prompt."
            )
        
    async def get_response(
                self, prompt: str, model_name: Optional[str] = None,
                effort: str = "minimal", verb: str = "low"
        ) -> Tuple[str, object]:
            model = model_name or self.model

            async def _call():
                return await self.client.responses.create(
                    model=model,
                    reasoning={"effort": effort},
                    text={"verbosity": verb},
                    instructions=self.system_prompt,
                    input=prompt,
                )

            resp = await self._with_retry(_call)
            return resp.output_text, resp.usage
        
        
    async def convert_to_json(self, freeform_playlist_text: str) -> str:
            async def _call():
                return await self.client.responses.create(
                    model=self.model,
                    reasoning={"effort": "minimal"},
                    text={"verbosity": "low"},
                    instructions=self.alt_sys_prompt,
                    input=freeform_playlist_text,
                )
            resp = await self._with_retry(_call)
            return resp.output_text

    async def _with_retry(self, fn: Callable[[], Awaitable[R]]) -> R:
            last_err = None
            for attempt in range(self.max_retries):
                try:
                    return await fn()
                except Exception as e:
                    last_err = e
                    # Decide if retryable
                    msg = str(e).lower()
                    status = getattr(e, "status_code", None) or getattr(e, "status", None)
                    retryable_status = {408, 409, 429, 500, 502, 503, 504}
                    code = str(getattr(e, "code", "") or "").lower()
                    invalid_prompt = (
                        status == 400 and (
                            "invalid_prompt" in code or "invalid prompt" in msg
                        )
                    )
                    is_retryable = (
                        (status in retryable_status)
                        or ("rate limit" in msg)
                        or ("retry" in msg)
                        or ("temporar" in msg)
                        or ("timeout" in msg)
                        or ("server error" in msg)
                        or invalid_prompt
                    )
                    if not is_retryable or attempt == self.max_retries - 1:
                        raise
                    # Prefer server-provided retry hints
                    delay = self._retry_after_from_error(e)
                    if delay is None:
                        # Exponential backoff with jitter
                        delay = self.backoff_base * (2 ** attempt) + random.uniform(0, 0.25)
                    await self._sleep(delay)
            raise last_err

    def _retry_after_from_error(self, err) -> Optional[float]:
            """Extract server-suggested delay (seconds) from error response headers, if any."""
            try:
                resp = getattr(err, "response", None)
                headers = getattr(resp, "headers", None)
                if not headers:
                    return None
                # Case-insensitive access
                h = {str(k).lower(): v for k, v in headers.items()}
                # Retry-After (seconds or HTTP date)
                ra = h.get("retry-after")
                if ra is not None:
                    try:
                        return float(ra)
                    except Exception:
                        # Possibly an HTTP-date; ignore for simplicity here
                        return None
                # OpenAI rate limit reset hints
                reset_req = h.get("x-ratelimit-reset-requests") or h.get("x-ratelimit-reset")
                if reset_req is not None:
                    try:
                        val = float(reset_req)
                        # Heuristic: treat small values as seconds; large as epoch
                        if val > 1e6:
                            return max(0.0, val - time.time())
                        return max(0.0, val)
                    except Exception:
                        return None
            except Exception:
                return None
            return None
