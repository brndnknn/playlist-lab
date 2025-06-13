import json
import csv
import time
from utils.helpers import has_keys, extract_array
from benchmarking.base_benchmark import BaseBenchmark

class OpenAIModelBenchmark(BaseBenchmark):
    def __init__(self, prompts, models, manager, output_csv, spotify_client):
        super().__init__(prompts, models, output_csv, spotify_client)
        self.manager = manager
        

    def run(self):
        for prompt in self.prompts:
            row = {"Prompt": prompt}
            unique_songs = set()

            for model in self.models:
                try:

                    start_time = time.time()
                    freeform_response, usage = self.manager.get_response(prompt)
                    runtime = time.time() - start_time


                    json_response = self.manager.convert_to_json(freeform_response)

                    playlist = self.validate_json(json_response)

                    valid, total, output_text = self.validate_tracks(playlist)

                    print(playlist)
                    row[model + ' - raw_text'] = freeform_response
                    row[model] = json.dumps(playlist, indent=2, ensure_ascii=False)
                    row[model + ' - runtime'] = f"{runtime:.2f}"

                    row[model + ' - tracks_parsed'] = total
                    row[model + ' - tracks_found'] = valid
                    row[model + ' - check_results'] = output_text

                    row[model + ' - input_tokens'] = usage.input_tokens
                    row[model + ' - output_tokens'] = usage.output_tokens
                    row[model + ' - total_tokens'] = usage.total_tokens


                    if isinstance(playlist, list):
                        for song in playlist:
                            
                            unique_songs.add((song['title'].strip(), song['artist'].strip()))

                except Exception as e:
                    row[model] = f"ERROR: {str(e)}"
            
            # combined = [{"title": t, "artist": a} for (t, a) in sorted(unique_songs)]
            # valid, total, output_text = self.validate_tracks(combined)

            # row["Combined"] = json.dumps(combined, indent=2, ensure_ascii=False)
            # row["Combined - tracks_parsed"] = total
            # row["Combined - tracks_found"] = valid
            # row["Combined - output_text"] = output_text
            

            self.results.append(row)

        fieldnames = set()

        for row in self.results:
            fieldnames.update(row.keys())
        fieldnames = ["Prompt"] + sorted(k for k in fieldnames if k != "Prompt")
        self.write_csv(fieldnames)




   