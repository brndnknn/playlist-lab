from typing import Optional, Tuple
import asyncio
from openai import AsyncOpenAI

class OpenAIAsyncManager:
    """
    Async twin of OpenAIManger. Same inputs/outputs, but awaitable.
    """
    def __init__(self, api_key: str, model: str = "gpt-5-nano"):
        self.model = model
        self.client = AsyncOpenAI(api_key=api_key)
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
            resp = await self.client.responses.create(
                model=model,
                reasoning={"effort": effort},
                text={"verbosity": verb},
                instructions=self.system_prompt,
                input=prompt,
            )
            return resp.output_text, resp.usage
        
        
    async def convert_to_json(self, freeform_playlist_text: str) -> str:
            resp = await self.client.responses.create(
                model=self.model,
                reasoning={"effort": "minimal"},
                text={"verbosity": "low"},
                instructions=self.alt_sys_prompt,
                input=freeform_playlist_text,
            )
            return resp.output_text