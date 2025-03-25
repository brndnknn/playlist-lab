import requests
import base64
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

class TokenHandler:
    def __init__(self):
        self.client_id = os.environ.get("SPOTIFY_CLIENT_ID")
        self.client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
        self.token_file = "token.json"
        self.token = {}


    def get_new_token(self):
        # Request a new token and save it locally
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
        
        token_time = token["expires_in"] + time
        token["expires_at"] = token_time

        with open("token.json", "w") as json_file:
            json.dump(token, json_file, indent=4, ensure_ascii=True)

    def check_token(self, token):

        current_time = time.time() - 60

        if token["expires_at"] > current_time:
            return True
        
        return False
    
    def load_token(self):
        
        if os.path.isfile(self.token_file):

            with open(self.token_file, 'r') as file:
                token = json.load(file)

            if self.check_token(token):
                return token
            
        current_time = time.time()
        token = self.get_new_token()
        self.save_token(token, current_time)

        return token