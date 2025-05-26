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

                    try:
                        playlist = json.loads(response)
                    except json.JSONDecodeError:
                        fixed_response = extract_array(response[1:])
                        try:
                            playlist = json.loads(fixed_response)
                        except json.JSONDecodeError:
                            print("JSON ERROR")
                            row[model] = "JSON ERROR"

                    print(playlist)
                    row[model] = json.dumps(playlist, ensure_ascii=False)
                    for song in playlist:
                        unique_songs.add((song['title'].strip(), song['artist'].strip()))

                except Exception as e:
                    row[model] = f"ERROR: {str(e)}"
            
            combined = [{"title": t, "artist": a} for (t, a) in sorted(unique_songs)]
            row["Combined"] = json.dumps(combined, ensure_ascii=False)

            self.results.append(row)

        self.write_csv(["Prompt"] + self.models + ["Combined"])



   