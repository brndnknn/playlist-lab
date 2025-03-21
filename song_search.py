import requests
import base64
import os
from dotenv import load_dotenv


# load environment variables from .env
load_dotenv()

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

def get_access_token():
    """
    Obtain a Spotify API access token using the Client Credentials flow.

    The Spotify Client ID and Client Secret should be stored in a .env file.

    Returns:
        str: A valid access token string.
    Raises:
        HTTPError: If the Spotify API returns a non-200 status code.
    """


    auth_string = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()

    token_info = response.json()
    return token_info["access_token"]


def track_exists(title, artist):
    """
    Check if a track with the given title and artist exists on Spotify.

    Args:
        title (str): The track title to search for.
        artist (str): The artist name for the track. 

    Returns:
        bool: True if a matching track is found, otherwise False.
    Raises:
        HTTPError: If the Spotify API returns a non-200 status code.
    """

    token = get_access_token()

    query = f"track:{title} artist:{artist}"

    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": query,
        "type": "track",
        "limit": 1
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    tracks = data.get("tracks", {}).get("items", [])

    # If at least one item exists, print the items and return true
    if tracks:
        print(tracks[0]["external_urls"])
        return True
    else:
        return False



if __name__ == "__main__":
    print(track_exists("Hotel California", "Eagles"))
    print(track_exists("FooBar", "BarFoo"))