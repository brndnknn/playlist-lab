"""
PlaylistGenAI — OpenAI Async Benchmark Entrypoint
=================================================

Runs the same benchmark as the sync entrypoint but executes OpenAI calls
concurrently using asyncio. Produces an identical CSV schema so results
are directly comparable to the sync runner.
"""

import os
import asyncio
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from playlist_generation.openai_async_manager import OpenAIAsyncManager
from benchmarking.openai_async_benchmark import OpenAIModelAsyncBenchmark
from api_clients.token_handler import TokenHandler
from api_clients.spotify_client import SpotifyClient
from utils.logger_config import set_log_file


load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


async def main_async():
    prompts = [
        "Darth Vader's tea party playlist",
    ]

    models = [
        "gpt-5-nano",
    ]

    # Create per-run output directory under repo-root/output/YYYYMMDD_HHMMSS
    repo_root = Path(__file__).resolve().parents[3]
    output_root = repo_root / "output"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = output_root / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)

    # Configure logging to file inside the run directory
    set_log_file(str(run_dir / "playlistGenAI.log"), mode="w")

    manager = OpenAIAsyncManager(API_KEY)
    csv_file_path = str(run_dir / "openai_benchmark_results_async.csv")

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
