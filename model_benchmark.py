import subprocess
import time
import csv
from llm_manager import OllamaManager

class ModelBenchmark:
    def __init__(self, models, prompts, output_csv=None):
        self.models = models
        self.prompts = prompts
        self.output_csv = output_csv
        self.results = []
        self.llm_manager = OllamaManager()

    def run_benchmarks(self):
        for model in self.models:
            for prompt in self.prompts:
                self.__run_single_test(model, prompt)

        if self.output_csv:
            self.__write_csv()

        #return self.results
    
    def __run_single_test(self, model, prompt):
        print(f"\n=== Testing model: {model} | Prompt: {prompt} ===")
        start_time = time.time()
        
        try:
            output_text = self.llm_manager.get_response(prompt, model)
            end_time = time.time()
            runtime = end_time - start_time

            # Log/print
            print(f"Time taken: {runtime:.2f} seconds")
            print(f"Model output:\n{output_text}\n")

            # Store for summary
            result = {
                "model": model,
                "prompt": prompt,
                "runtime_sec": runtime,
                "output": output_text
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
                "output": f"ERROR: {error_msg}"
            }

            self.results.append(result)

    def __write_csv(self):
        """
        Write results to CSV.
        """
        with open(self.output_csv, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["model", "prompt", "runtime_sec", "output"])
            writer.writeheader()
            writer.writerows(self.results)
