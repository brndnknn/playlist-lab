"""
Runs benchmarks for OpenAI LLMs on playlist generation prompts.

Generates playlists, collects metrics, validates tracks, and writes detailed
and summary results to CSV.
"""

import json
import time
import itertools
from benchmarking.base_benchmark import BaseBenchmark

class OpenAIModelBenchmark(BaseBenchmark):
    def __init__(self, prompts, models, manager, output_csv, spotify_client):
        """
        Initializes the OpenAIModelBenchmark.

        Args:
            prompts (list): List of prompt strings.
            models (list): List of OpenAI model names.
            manager (OpenAIManager): For calling OpenAI models.
            output_csv (str): Path to output CSV.
            spotify_client (SpotifyClient): For validating tracks.
        """
        super().__init__(prompts, models, output_csv, spotify_client)
        self.manager = manager
        self.effort = ["minimal", "low"]
        self.verb = ["low"]

        self.fieldnames = [
            "prompt",
            "model",
            "effort",
            "verbosity",
            "raw_text",
            "json",
            "check_results",

            "runtime",
            "tracks_parsed",
            "tracks_found",
            
            "input_tokens",
            "output_tokens",
            "total_tokens"

        ]
        

    def run(self):
        """
        Runs the OpenAI playlist generation benchmarks and writes results to CSV.
        """
        for prompt in self.prompts:
            for model, effort, verb in itertools.product(self.models, self.effort, self.verb):
                row = {"prompt": prompt}
                try:

                    start_time = time.time()
                    freeform_response, usage = self.manager.get_response(prompt, model, effort, verb)
                    runtime = time.time() - start_time


                    json_response = self.manager.convert_to_json(freeform_response)

                    playlist = self.validate_json(json_response)

                    valid, total, output_text = self.validate_tracks(playlist)

                    print(playlist)
                    
                    row["model"] = model
                    row["effort"] = effort
                    row["verbosity"] = verb
                    row['raw_text'] = freeform_response
                    row["json"] = json.dumps(playlist, indent=2, ensure_ascii=False)
                    row['check_results'] = output_text
                    
                    row['runtime'] = f"{runtime:.2f}"
                    row['tracks_parsed'] = total
                    row['tracks_found'] = valid
                    

                    row['input_tokens'] = usage.input_tokens
                    row['output_tokens'] = usage.output_tokens
                    row['total_tokens'] = usage.total_tokens

                except Exception as e:
                    row['model'] = f"ERROR: {str(e)}"

                self.results.append(row)

        self.write_csv(self.fieldnames)




   