import subprocess
import time
import csv
from llm_manager import OllamaManager

def benchmark_models(models, prompts, output_csv=None):
    """
    Test different models using Ollama, measuring time to get a response and capturing the text output.

    :param models: List of model names recognized by Ollama.
    :param prompt: String prompt to provide to each model.
    "param output_csv: (Optional) Path to a CSV file to save the results.
    """

    results = []

    llm_manager = OllamaManager()

    for model in models: 
        for prompt in prompts:
            print(f"\n=== Testing model: {model} | Prompt: {prompt} ===")
            start_time = time.time()

            try:
                output_text = llm_manager.get_response(prompt, model)
                end_time = time.time()

                # Gather stats
                runtime = end_time - start_time

                # Log/print
                print(f"Time taken: {runtime:.2f} seconds")
                print(f"Model output:\n{output_text}\n")

                # Store for summary
                results.append({
                    "model": model,
                    "prompt": prompt,
                    "runtime_sec": runtime,
                    "output": output_text
                })
            except subprocess.CalledProcessError as e:
                # If there's an error running the command, store that info too
                end_time = time.time()
                runtime = end_time - start_time
                error_msg = e.stderr.strip() if e.stderr else "Unknown error"

                print(f"Error calling Ollama with model '{model}': {error_msg}")
                results.append({
                    "model": model,
                    "prompt": prompt,
                    "runtime_sec": runtime,
                    "output": f"ERROR: {error_msg}"
                })

    # Optionally, write results to CSV
    if output_csv:
        with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["model", "prompt", "runtime_sec", "output"])
            writer.writeheader()
            writer.writerows(results)

    return results

if __name__ == "__main__":

    # list of models to test
    models_to_test = [
        "llama3.2:1b",
        "llama3.2:latest",
        "gemma3:1b", 
        "gemma3:latest",
        "gemma2:2b",
        "mistral:latest"
    ]  

    # list of prompts to test
    prompts_to_test = [
        "Generate a short playlist of 5 real pop songs from the 2010s.",
        "Suggest 10 upbeat rock songs for a workout playlist",
        "I want a playlist of songs with acoustic guitars and an angry mood"
    ]

    csv_file_path = "ollama_benchmark_results.csv"

    summary = benchmark_models(models=models_to_test,
                               prompts=prompts_to_test,
                               output_csv=csv_file_path)
    
    print("\n=== Summary of Results ===")
    for result in summary:
        print(f"Model: {result['model']} | Prompt: {result['prompt']}",
              f"Time: {result['runtime_sec']:.2f}s",
              f"Output: {result['output'][:100]}...")


