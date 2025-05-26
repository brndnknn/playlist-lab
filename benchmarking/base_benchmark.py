import csv

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