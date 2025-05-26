import json
import csv
from utils.helpers import has_keys, extract_array
from benchmarking.base_benchmark import BaseBenchmark

class OpenAIModelBenchmark(BaseBenchmark):
    def __init__(self, prompts, models, manager, output_csv):
        super().__init__(prompts, models, output_csv)
        self.manager = manager

    def run(self):
        for prompt in self.prompts:
            row = {"Prompt": prompt}
            unique_songs = set()

            for model in self.models:
                try:
                    response = self.manager.get_response(prompt)

                    playlist = self.validate_json(response)

                    print(playlist)
                    row[model] = json.dumps(playlist, ensure_ascii=False)
                    if isinstance(playlist, list):
                        for song in playlist:
                            unique_songs.add((song['title'].strip(), song['artist'].strip()))

                except Exception as e:
                    row[model] = f"ERROR: {str(e)}"
            
            combined = [{"title": t, "artist": a} for (t, a) in sorted(unique_songs)]
            row["Combined"] = json.dumps(combined, ensure_ascii=False)

            self.results.append(row)

        self.write_csv(["Prompt"] + self.models + ["Combined"])



   