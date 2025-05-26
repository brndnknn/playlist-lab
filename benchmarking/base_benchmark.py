import csv
import json
from utils.helpers import extract_array

class BaseBenchmark:
    def __init__(self, prompts, models, output_csv):
        self.prompts = prompts
        self.models = models
        self.output_csv = output_csv
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

        
        