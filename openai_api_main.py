import os
from benchmarking.openai_benchmark import OpenAIModelBenchmark
from dotenv import load_dotenv
from playlist_generation.OpenAIManager import OpenAIManager

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


def main():
    prompts = [
        # "Playlist for aliens trying to blend in at a human barbecue",
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
        # "Playlist for aliens first encountering human pizza",
        # "What music plays in Shrek’s mind while he's meditating",
        "Songs to listen to while seductively making a sandwich"
    ]

    models = [
        "gpt-4.1",
        "gpt-4o",
        "gpt-4.5-preview"
    ]


    manager = OpenAIManager(api_key)
    benchmark = OpenAIModelBenchmark(prompts, models, manager, "openai_benchmark_results.csv")
    benchmark.run()


if __name__ == "__main__":
    main()