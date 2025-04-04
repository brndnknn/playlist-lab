import subprocess
import requests
import time
from helpers import extract_array


class OllamaManager:
    """
    Manages interactions with the Ollama Server, allowing the user to run prompts on specified LLM models and retrieve text responses.
    """

    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.system_prompt = "Respond in JSON. Each song should be represented by an object with a 'title' and 'artist'."

    def start_ollama_server(self, model):
        print("Starting Ollama server...")
        subprocess.Popen(["ollama", "serve"], stderr=subprocess.DEVNULL)
        for i in range(20):
            if self.is_ollama_running(model):
                print(f"Ollama server is up and running {model}")
                return
            print(f"Waiting for server..{'.' * (i + 1)}")
            time.sleep(6)
        raise RuntimeError("Ollama server failed to start after 10 seconds.")

    def is_ollama_running(self, model):
        try:
            r = requests.post(self.url, json={"model": model, "prompt": "", "stream": False}, timeout=1)
            return r.status_code == 200
        except requests.exceptions.RequestException:
            return False
        
    def get_response(self, model, prompt):
        full_prompt = prompt + " " + self.system_prompt
        payload = {
            "model": model,
            "prompt": full_prompt,
            "format": "json",
            "stream": False
        }
        print(payload)

        raw_response = requests.post(self.url, json=payload)
        raw_response.raise_for_status()
        raw_json_string = raw_response.json()['response']

        response = extract_array(raw_json_string)

        return response

