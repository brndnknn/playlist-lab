"""
PlaylistGenAI — Ollama Benchmark Runner
=======================================

Command-line entry point that benchmarks one or more locally hosted
Ollama LLM models against a curated list of playlist prompts.  
For every *(model, prompt)* pair it measures and records:

* End-to-end generation latency
* JSON-format correctness of the model output
* Real-world track coverage via live Spotify look-ups

Key collaborators
-----------------
• **TokenHandler** – acquires/caches Spotify API tokens  
• **SpotifyClient** – validates that each suggested track exists on Spotify  
• **ModelBenchmark** – orchestrates prompts, collects metrics,  
  and writes *ollama_benchmark_results.csv*

Run this file directly to regenerate the CSV and console-print progress.
"""



from benchmarking.model_benchmark import ModelBenchmark
from api_clients.token_handler import TokenHandler
from api_clients.spotify_client import SpotifyClient

def main():
    """Run the full Ollama model benchmark matrix.

    Workflow
    --------
    1. Define `models_to_test` and `prompts_to_test`.
    2. Fetch or refresh a Spotify token with :class:`TokenHandler`.
    3. Build a :class:`SpotifyClient` for per-track validation.
    4. Instantiate :class:`ModelBenchmark` and invoke
       :py:meth:`ModelBenchmark.run_benchmarks`.
    5. Persist detailed rows **plus** model/prompt summaries to
       *ollama_benchmark_results.csv*.

    All heavy lifting happens inside :class:`ModelBenchmark`; this
    function simply wires the components together.
    """
    
    # list of models to test
    models_to_test = [
        'gemma2:2b',
        # 'llama3.2:latest',
        # 'gemma3:latest',
        # 'llama3.2:3b-instruct-q8_0',
        # 'mistral:latest',
        # 'gemma3:4b-it-q8_0',
    ]  

    # list of prompts to test
    prompts_to_test = [
        "Playlist for aliens trying to blend in at a human barbecue",
        # "The Joker’s grocery shopping playlist",
        # "Songs your microwave would choose if it gained sentience",
        # "Music for awkward elevator rides with strangers",
        # "Songs to pretend you're the main character in a rom-com",
        # "Playlist for aggressively matching Tupperware lids",
        # "Playlist for a wizard accidentally trapped in the modern world",
        # "Songs you'd hear at a boring office birthday party",
        # "Songs for cats secretly planning to overthrow humanity",
        # "Playlist for Sherlock Holmes solving the case of missing socks",
        # "The robot uprising’s battle playlist (but it’s all disco)",
        # "Music for dramatically flipping through magazines in waiting rooms",
        # "Playlist for aliens trying human pizza for the first time",
        # "What music plays in Shrek’s mind while he's meditating",
        # "Songs to listen to while seductively making a sandwich"
    ]

    csv_file_path = "ollama_benchmark_results.csv"

    token_handler = TokenHandler()

    token = token_handler.load_token()

    spotify_client = SpotifyClient(token)

    benchmarker = ModelBenchmark(models=models_to_test,
                               prompts=prompts_to_test,
                               output_csv=csv_file_path, spotify_client=spotify_client)
    benchmarker.run_benchmarks()
        
if __name__ == "__main__":
    main()