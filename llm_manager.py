import subprocess
import requests
import time
from helpers import extract_array
from helpers import logged_request

class OllamaManager:
    """
    Manages interactions with the Ollama Server, allowing the user to run prompts on specified LLM models and retrieve text responses.
    """

    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.system_prompt = "Respond in JSON. The list of songs should be returned in an array. Each song should be represented by an object with the keys 'title' and 'artist'. "

    def start_ollama_server(self, model):
        print("Starting Ollama server...")
        self.kill_ollama_servers()
        subprocess.Popen(["ollama", "serve"], stderr=subprocess.DEVNULL)
        for i in range(20):
            if self.is_ollama_running(model):
                print(f"Ollama server is up and running {model}")
                return
            print(f"Waiting for server..{'.' * (i + 1)}")
            time.sleep(3)
        raise RuntimeError("Ollama server failed to start after 60 seconds.")

    def is_ollama_running(self, model):
        try:
            r = logged_request("POST", self.url, json={"model": model, "prompt": "", "stream": False}, timeout=5)
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

        try:
            raw_response = logged_request("POST", self.url, json=payload, timeout=180)
            raw_response.raise_for_status()
            raw_json_string = raw_response.json()['response']

            response = extract_array(raw_json_string)

            return response
        except:
            return {"error": "The request timed out after 3 mins"}
        
    def kill_ollama_servers(self):
        """
        Finds and kills any running Ollama server processes.
        """
        print("Checking if Ollama is running...")
        servers = subprocess.run(["pgrep", "ollama"], capture_output=True, text=True)
        if servers.returncode == 0:
            print("Found ollama running...")
            try:
                subprocess.run(["pkill", "-9" ,"ollama"], check=True)
                print("All Ollama processes killed.")
            except:
                print("Couldn't kill Ollama.")
        else:
            print("No Ollama processes found.")


