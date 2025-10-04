"""
Async benchmark runner for OpenAI LLMs on playlist generation.

Mirrors OpenAIModelBenchmark but executes model calls concurrently
using asyncio and a semaphore to control concurrency.
"""

import json
import time
import asyncio
import itertools
from typing import List
from tqdm import tqdm

from benchmarking.base_benchmark import BaseBenchmark


class OpenAIModelAsyncBenchmark(BaseBenchmark):
    def __init__(self, prompts: List[str], models: List[str], manager, output_csv: str, spotify_client, effort=None, verb=None):
        super().__init__(prompts, models, output_csv, spotify_client)
        self.manager = manager
        self.effort = effort or ["minimal"]
        self.verb = verb or ["low"]

        self.fieldnames = [
            "prompt",
            "model",
            "effort",
            "verbosity",
            "raw_text",
            "json",
            "check_results",
            "runtime",
            "tracks_parsed",
            "tracks_found",
            "input_tokens",
            "output_tokens",
            "total_tokens",
        ]

    async def _run_single(self, prompt: str, model: str, effort: str, verb: str, sem: asyncio.Semaphore):
        row = {"prompt": prompt}
        async with sem:
            try:
                start_time = time.time()
                freeform_response, usage = await self.manager.get_response(prompt, model, effort, verb)
                runtime = time.time() - start_time

                json_response = await self.manager.convert_to_json(freeform_response)
                playlist = self.validate_json(json_response)

                # Offload blocking Spotify checks to a thread to avoid blocking the event loop
                valid, total, output_text = await asyncio.to_thread(self.validate_tracks, playlist)

                row["model"] = model
                row["effort"] = effort
                row["verbosity"] = verb
                row["raw_text"] = freeform_response
                row["json"] = json.dumps(playlist, indent=2, ensure_ascii=False)
                row["check_results"] = output_text
                row["runtime"] = f"{runtime:.2f}"
                row["tracks_parsed"] = total
                row["tracks_found"] = valid

                # Usage object may vary; attempt attribute access with fallback
                try:
                    row["input_tokens"] = getattr(usage, "input_tokens", None)
                    row["output_tokens"] = getattr(usage, "output_tokens", None)
                    row["total_tokens"] = getattr(usage, "total_tokens", None)
                except Exception:
                    row["input_tokens"] = row["output_tokens"] = row["total_tokens"] = None

            except Exception as e:
                row["model"] = f"ERROR: {str(e)}"

        return row

    async def run(self, concurrency: int = 5):
        """
        Executes the async benchmark with limited concurrency and writes CSV.

        Args:
            concurrency (int): Maximum number of concurrent OpenAI requests.
        """
        combos = list(itertools.product(self.prompts, self.models, self.effort, self.verb))
        total = len(combos)
        sem = asyncio.Semaphore(concurrency)

        # Prepare tasks
        tasks = [self._run_single(prompt, model, effort, verb, sem) for (prompt, model, effort, verb) in combos]

        self.reset_results()
        self.initialize_csv(self.fieldnames)
        with tqdm(total=total, desc="OpenAI async benchmarks", unit="run", dynamic_ncols=True) as pbar:
            for coro in asyncio.as_completed(tasks):
                row = await coro
                self.record_result(row)
                pbar.update(1)
