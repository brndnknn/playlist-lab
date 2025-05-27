import csv
import json
from utils.helpers import extract_array, has_keys

class BaseBenchmark:
    def __init__(self, prompts, models, output_csv, spotify_client):
        self.prompts = prompts
        self.models = models
        self.output_csv = output_csv
        self.spotify_client = spotify_client
        self.results = []

    def write_csv(self, fieldnames):
        
        with open(self.output_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.results)

    def validate_json(self, input_text):

        try:
            playlist = json.loads(input_text)

        except json.JSONDecodeError:
            fixed_text = extract_array(input_text[1:])
            try:
                playlist = json.loads(fixed_text)
            except json.JSONDecodeError:
                return f"JSON ERROR \n {input_text}"

        return playlist

    def validate_tracks(self, playlist):
        valid, total = 0, 0
        output_text = ""

        if not isinstance(playlist, list):
            return (valid, total, playlist)

        for track in playlist:
            if has_keys(track, "title", "artist"):
                total += 1
                results = self.spotify_client.track_exists(track["title"], track["artist"])
                if results[0] == True:
                    valid += 1
                output_text = output_text + results[1] + '\n'
        
        return(valid, total, output_text)

        
        