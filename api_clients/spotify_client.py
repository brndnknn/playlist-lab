from utils.logger_config import logger
from utils.helpers import logged_request
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

        logger.info(f"Searching Spotify for: {title} by {artist}")
        try:
            response = logged_request("GET", url, headers=headers, params=params)

            data = response.json()

            tracks = data.get("tracks", {}).get("items", [])

            # If at least one item exists, print the items and return true
            if tracks:
                print(title, artist)
                print(tracks[0]["external_urls"])
                print()
                output_text = (f"{title}, {artist}, {tracks[0]['external_urls']}")
                return [True, output_text]
            else:
                print("Search failed")
                print(title, artist)
                print()
                output_text = (f"{title}, {artist}, Search failed")
                return [False, output_text]
            
        except Exception as e:
            logger.error(f"HTTP Error {e}, skipping this track")
            return [False, f"HTTP Error while searching for {title}, {artist}."]

