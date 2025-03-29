import requests
from token_handler import TokenHandler

class SpotifyClient:
    """
    Provides methods to interact with the Spotify Web API, 
    such as checking if a given track exists.
    """

    def __init__(self, token):
        """
        Initializes the SpotifyClient with a pre-fetched Spotify token.

        Args:
            token (dict): A dictionary containing at least 'access_token', 
                which is used to authenticate requests to Spotify.
        """
        self.token = token

    def track_exists(self, title, artist):
        """
        Checks if a track with the given title and artist exists on Spotify.

        Args:
            title (str): The track title.
            artist (str): The artist name for the track.

        Returns:
            bool: True if a matching track is found on Spotify, otherwise False.

        Raises:
            requests.HTTPError: If the Spotify API returns a non-200 status code.
        """
        query = f"track:{title} artist:{artist}"
        url = "https://api.spotify.com/v1/search"
        headers = {
            "Authorization": f"Bearer {self.token['access_token']}"
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

