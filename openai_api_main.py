import os
from dotenv import load_dotenv
from playlist_generation.OpenAIManager import OpenAIManager

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
def main():

    playlistGen = OpenAIManager(api_key)

    prompt = input("Enter a playlist description: ")

    playlist = playlistGen.get_response(prompt)

    print(playlist)


if __name__ == "__main__":
    main()