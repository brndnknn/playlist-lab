import subprocess

class OllamaManager:
    def __init__(self):
        self.system_instructions = """
# system
You are a playlist generator. Please output ONLY the list of songs. Each song should have a title in quotes followed by a dash and then the artist name. No extra commentary, disclaimers, or reasoning.

# user

"""

    def get_response(self, prompt, model):
        """
        Run Ollama with the specified model and prompt. Returns the model's text output.
        """

        full_prompt = self.system_instructions + prompt

        cmd = [
            "ollama", "run",
            model, full_prompt
        ]

        process = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return process.stdout.strip()