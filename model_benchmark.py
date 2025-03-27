import subprocess
import time
import csv
import re
from llm_manager import OllamaManager
from spotify_client import SpotifyClient

class ModelBenchmark:
    def __init__(self, models, prompts, output_csv, spotify_client):
        self.models = models
        self.prompts = prompts
        self.output_csv = output_csv
        self.results = []
        self.llm_manager = OllamaManager()
        self.spotify_client = spotify_client

    def run_benchmarks(self):
        for model in self.models:
            for prompt in self.prompts:
                self.__run_single_test(model, prompt)

        if self.output_csv:
            self.__write_csv()

    def __run_single_test(self, model, prompt):
        print(f"\n=== Testing model: {model} | Prompt: {prompt} ===")
        start_time = time.time()
        
        try:
            output_text = self.llm_manager.get_response(prompt, model)
            end_time = time.time()
            runtime = end_time - start_time

            valid_tracks , total_tracks = self.__validate_tracks(output_text)

            # Log/print
            print(f"Time taken: {runtime:.2f} seconds")
            print(f"Model output:\n{output_text}\n")
            print(f"Tracks parsed: {total_tracks}, tracks found on Spotify: {valid_tracks}")

            # Store for summary
            result = {
                "model": model,
                "prompt": prompt,
                "runtime_sec": runtime,
                "output": output_text,
                "tracks_parsed": total_tracks,
                "tracks_found": valid_tracks
            }

            self.results.append(result)
        
        except subprocess.CalledProcessError as e:
            # If there's an error running the command, store that info too
            end_time = time.time()
            runtime = end_time - start_time
            error_msg = e.stderr.strip() if e.stderr else "Unknown error"
            
            print(f"Error calling Ollama with model '{model}': {error_msg}")

            result = {
                "model": model,
                "prompt": prompt,
                "runtime_sec": runtime,
                "output": f"ERROR: {error_msg}",
                "tracks_parsed": 0,
                "tracks_found": 0
            }

            self.results.append(result)

    def __write_csv(self):
        """
        Write results to CSV.
        """
        with open(self.output_csv, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "model",
                "prompt",
                "runtime_sec",
                "output",
                "tracks_parsed",
                "tracks_found"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.results)

    def __validate_tracks(self, output_text):

        lines = output_text.split('\n')
        pattern = re.compile(r'^\"(?P<title>[^\"]+)\"\s*-\s*(?P<artist>.+)$')

        total = 0
        valid = 0
        for line in lines:
            match = pattern.match(line.strip())
            if match: 
                total += 1
                title = match.group('title')
                artist = match.group('artist')
                if self.spotify_client.track_exists(title, artist):
                    valid += 1
        return (valid, total)
