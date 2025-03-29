from model_benchmark import ModelBenchmark
from token_handler import TokenHandler
from spotify_client import SpotifyClient

def main():
    """
    Main entry point to run the LLM model benchmarks with 
    specified models and prompts.

    Loads a valid Spotify API token, constructs the SpotifyClient
    and ModelBenchmark classes, and runs the benchmarks.
    """
    
    # list of models to test
    models_to_test = [
        "llama3.2:1b",
        # "llama3.2:latest",
        "gemma3:1b", 
        # "gemma3:latest",
        "gemma2:2b",
        # "mistral:latest"
    ]  

    # list of prompts to test
    prompts_to_test = [
        "Generate a short playlist of 5 real pop songs from the 2010s.",
        "Suggest 10 upbeat rock songs for a workout playlist",
        "I want a playlist of acoustic songs with an angry mood"
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