from model_benchmark import ModelBenchmark

def main():

    # list of models to test
    models_to_test = [
        "llama3.2:1b",
        # "llama3.2:latest",
        "gemma3:1b", 
        # "gemma3:latest",
        "gemma2:2b",
        # "mistral:latest"
    ]  

    # list of prompts to test
    prompts_to_test = [
        "Generate a short playlist of 5 real pop songs from the 2010s.",
        "Suggest 10 upbeat rock songs for a workout playlist",
        "I want a playlist of acoustic songs with an angry mood"
    ]

    csv_file_path = "ollama_benchmark_results.csv"

    benchmarker = ModelBenchmark(models=models_to_test,
                               prompts=prompts_to_test,
                               output_csv=csv_file_path)
    summary = benchmarker.run_benchmarks()
    
    # print("\n=== Summary of Results ===")
    # for result in summary:
    #     print(f"Model: {result['model']} | Prompt: {result['prompt']}",
    #           f"Time: {result['runtime_sec']:.2f}s",
    #           f"Output: {result['output'][:100]}...")
        
if __name__ == "__main__":
    main()