import requests
from token_handler import TokenHandler


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

    spotify_token = TokenHandler()
    token = spotify_token.load_token()

    query = f"track:{title} artist:{artist}"

    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token['access_token']}"
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