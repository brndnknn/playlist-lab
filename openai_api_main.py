import os
from benchmarking.openai_benchmark import OpenAIModelBenchmark
from dotenv import load_dotenv
from playlist_generation.OpenAIManager import OpenAIManager
from api_clients.token_handler import TokenHandler
from api_clients.spotify_client import SpotifyClient

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


def main():
    prompts = [
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

    models = [
        "gpt-4.1",
        "gpt-4.1-mini",
        # "gpt-4o",
        # "gpt-4o-mini",
        # "gpt-4.5-preview"
    ]


    manager = OpenAIManager(api_key)
    csv_file_path = "openai_benchmark_results.csv"
    
    token_handler = TokenHandler()
    token = token_handler.load_token()

    spotify_client = SpotifyClient(token)


    benchmark = OpenAIModelBenchmark(prompts, models,
                                     manager, csv_file_path,
                                     spotify_client)
    benchmark.run()


if __name__ == "__main__":
    main()