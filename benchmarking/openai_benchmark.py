import json
import csv
from utils.helpers import has_keys, extract_array

class OpenAIModelBenchmark:
    def __init__(self, prompts, models, manager, output_csv):
        """
        :param prompts: List of prompt strings to use
        :param models: List of OpenAI model names
        :param manager: An instance of OpenAIManager
        :param output_csv: Path to CSV output file
        """
        self.prompts = prompts
        self.models = models
        self.manager = manager
        self.output_csv = output_csv
        self.results = []

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

        self._write_csv()

    def _write_csv(self):
        fieldnames = ["Prompt"] + self.models + ["Combined"]
        with open(self.output_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.results)

   