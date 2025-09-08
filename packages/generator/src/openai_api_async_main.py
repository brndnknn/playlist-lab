"""
PlaylistGenAI — OpenAI Async Benchmark Entrypoint
=================================================

Runs the same benchmark as the sync entrypoint but executes OpenAI calls
concurrently using asyncio. Produces an identical CSV schema so results
are directly comparable to the sync runner.
"""

import os
import asyncio
from dotenv import load_dotenv

from playlist_generation.openai_async_manager import OpenAIAsyncManager
from benchmarking.openai_async_benchmark import OpenAIModelAsyncBenchmark
from api_clients.token_handler import TokenHandler
from api_clients.spotify_client import SpotifyClient


load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


async def main_async():
    prompts = [
        "Darth Vader's tea party playlist",
    ]

    models = [
        "gpt-5-nano",
    ]

    manager = OpenAIAsyncManager(API_KEY)
    csv_file_path = "openai_benchmark_results_async.csv"

    token_handler = TokenHandler()
    token = token_handler.load_token()
    spotify_client = SpotifyClient(token)

    benchmark = OpenAIModelAsyncBenchmark(
        prompts=prompts,
        models=models,
        manager=manager,
        output_csv=csv_file_path,
        spotify_client=spotify_client,
    )

    await benchmark.run(concurrency=5)


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()

