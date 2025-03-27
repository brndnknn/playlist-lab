import requests
from token_handler import TokenHandler

class SpotifyClient:
    def __init__(self, token):
        self.token = token

    def track_exists(self, title, artist):

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

