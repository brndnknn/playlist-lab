import subprocess
import time
import csv

def benchmark_models(models, prompt, output_csv=None):
    """
    Test different models using Ollama, measuring time to get a response and capturing the text output.

    :param models: List of model names recognized by Ollama.
    :param prompt: String prompt to provide to each model.
    "param output_csv: (Optional) Path to a CSV file to save the results.
    """

    results = []

    for model in models: 
        print(f"\n=== Testing model: {model} ===")
        start_time = time.time()

        # Example ollama command:
        #   ollama run --model <model_name> "<prompt>"
        # Output will be captured using subprocess.
        cmd = [
            "ollama", "run", model, prompt
        ]

        try:
            process = subprocess.run(cmd, capture_output=True, text=True, check=True)
            end_time = time.time()

            # Gather stats
            runtime = end_time - start_time
            output_text = process.stdout.strip()

            # Log/print
            print(f"Time taken: {runtime:.2f} seconds")
            print(f"Model output:\n{output_text}\n")

            # Store for summary
            results.append({
                "model": model,
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
                "runtime_sec": runtime,
                "output": f"ERROR: {error_msg}"
            })

    # Optionally, write results to CSV
    if output_csv:
        with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["model", "runtime_sec", "output"])
            writer.writeheader()
            writer.writerows(results)

    return results

if __name__ == "__main__":
    models_to_test = [
        "llama3.2:1b",
        "llama3.2:latest"
    ]

    test_prompt = "Generate a short playlist of 5 real pop songs from the 2010s."

    csv_file_path = "ollama_benchmark_results.csv"

    summary = benchmark_models(models=models_to_test,
                               prompt=test_prompt,
                               output_csv=csv_file_path)
    
    print("\n=== Summary of Results ===")
    for result in summary:
        print(f"Model: {result['model']}",
              f"Time: {result['runtime_sec']:.2f}s",
              f"Output: {result['output'][:100]}...")


