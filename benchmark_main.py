from benchmarking.model_benchmark import ModelBenchmark
from api_clients.token_handler import TokenHandler
from api_clients.spotify_client import SpotifyClient

def main():
    """
    Main entry point to run the LLM model benchmarks with 
    specified models and prompts.

    Loads a valid Spotify API token, constructs the SpotifyClient
    and ModelBenchmark classes, and runs the benchmarks.
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

        # Easy & Straightforward:
        "Create a playlist of upbeat indie pop songs.",
        "Generate a playlist with songs by artists known for their synth-pop sound.",
        # "Give me a playlist with some classic rock anthems.",
        # "I want a playlist with a chill vibe, mainly focusing on acoustic music.",
        # "Suggest a playlist with songs by female vocalists."

        # # Medium Complexity:
        # "Generate a playlist that reflects a feeling of nostalgia for the 80s.",
        # "Create a playlist with songs that are generally upbeat and energetic.",
        # "Give me a playlist centered around the themes of heartbreak and loss.",
        # "I'm looking for a playlist with a blend of electronic dance music and chillwave.",
        # "Suggest a playlist that captures the feeling of a summer road trip.",


        # # Advanced & Abstract (Good for checking nuance & creativity):
        # "Imagine Napoleon Bonaparte was listening to Spotify in the 19th century. Create a playlist of songs he would have listend to while conquering the Alps",
        # "Create a playlist evoking the atmosphere of a dimly lit jazz club in 1960s New Orleans. Include songs with a melancholic feel and soulful instrumentation.",
        # "Design a playlist representing a journey through a digital dreamscape. Think neon colors, glitch effects, and fragmented melodies.",
        # "Craft a playlist that embodies the spirit of cyberpunk - a blend of dark, atmospheric soundscapes, electronic rhythms, and gritty samples.",
        # "Generate a playlist that simulates a rainy afternoon in a small European town, focusing on themes of introspection and quiet observation.",

        # # Bonus - For really pushing the boundaries:**
        # "Compose a playlist that tells the story of a lost lighthouse keeper, inspired by the isolation and beauty of the sea."
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