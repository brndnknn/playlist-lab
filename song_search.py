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
    print(auth_string)
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


if __name__ == "__main__":
    print(get_access_token())