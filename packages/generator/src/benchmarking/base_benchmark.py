"""
Base class for benchmarking LLMs on playlist generation tasks.

Provides common methods for running prompts, writing CSV results,
validating JSON outputs, and checking playlist tracks against Spotify.
"""

import csv
import json
from pathlib import Path
from utils.helpers import extract_array, has_keys

class BaseBenchmark:
    def __init__(self, prompts, models, output_csv, spotify_client):
        """
        Initializes the BaseBenchmark with prompts, models, and I/O configuration.

        Args:
            prompts (list): List of playlist prompt strings.
            models (list): List of model names to benchmark.
            output_csv (str): Path to the output CSV file.
            spotify_client (SpotifyClient): Instance for validating tracks on Spotify.
        """
        self.prompts = prompts
        self.models = models
        self.output_csv = output_csv
        self.spotify_client = spotify_client
        self.results = []

    def write_csv(self, fieldnames):
        """
        Writes benchmark results to a CSV file.

        Args:
            fieldnames (list): List of CSV column headers.
        """
        # Ensure parent directory exists if a nested path was provided
        try:
            parent = Path(self.output_csv).parent
            if str(parent) and str(parent) != ".":
                parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            # If output_csv is a bare filename or parent creation fails, proceed to open
            pass

        with open(self.output_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.results)

    def validate_json(self, input_text):
        """
        Attempts to load and repair a playlist from a JSON string.

        Args:
            input_text (str): The model's raw output string.

        Returns:
            object: Parsed playlist object (list or error string).
        """
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
        """
        Checks if each track in the playlist exists on Spotify.

        Args:
            playlist (list): List of track dicts with 'title' and 'artist'.

        Returns:
            tuple: (int valid, int total, str output_text)
        """
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

        
        
