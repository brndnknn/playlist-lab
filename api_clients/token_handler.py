import requests
import base64
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

class TokenHandler:
    """
    Responsible for obtaining and storing a Spotify API access token 
    via the client credentials flow, and ensuring it's valid before use.
    """
    
    def __init__(self):
        """
        Initializes the TokenHandler by reading Spotify client credentials 
        from environment variables and setting up file paths for token storage.
        """
        self.client_id = os.environ.get("SPOTIFY_CLIENT_ID")
        self.client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
        self.token_file = "../token.json"
        self.token = {}


    def get_new_token(self):
        """
        Requests a new token from Spotify using the client credentials flow.

        Returns:
            dict: The JSON response containing the new token data.

        Raises:
            requests.HTTPError: If the request to Spotify fails or 
                returns an error status code.
        """
        auth_string = f"{self.client_id}:{self.client_secret}"
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

        return response.json()
    

    def save_token(self, token, time):
        """
        Saves the token data to a local JSON file, 
        adding an 'expires_at' timestamp.

        Args:
            token (dict): The token data received from Spotify.
            current_time (float): The current Unix epoch time.
        """
        token_time = token["expires_in"] + time
        token["expires_at"] = token_time

        with open("token.json", "w") as json_file:
            json.dump(token, json_file, indent=4, ensure_ascii=True)

    def check_token(self, token):
        """
        Checks if the given token is still valid.

        Args:
            token (dict): The token data from file.

        Returns:
            bool: True if the token is not expired, otherwise False.
        """
        current_time = time.time() - 60

        if token["expires_at"] > current_time:
            return True
        
        return False
    
    def load_token(self):
        """
        Loads a valid token from the local file if it exists and is still valid. Otherwise, request a new token and saves it.
        
        Returns:
            dict: The valid token data (includes 'access_token).
        """
        if os.path.isfile(self.token_file):

            with open(self.token_file, 'r') as file:
                token = json.load(file)

            if self.check_token(token):
                return token
            
        current_time = time.time()
        token = self.get_new_token()
        self.save_token(token, current_time)

        return token