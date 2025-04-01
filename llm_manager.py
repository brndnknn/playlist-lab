import subprocess

class OllamaManager:
    """
    Manages interactions with the Ollama CLI, allowing the user to run prompts on specified LLM models and retrieve text responses.
    """



    def __init__(self):
        """
        Initializes the OllamaManager with default system instructions. 
        
        The system_instructions attribute is prepended to the user's prompt before calling ollama run. It instructs the model to output only a formatted list of songs, with minial commentary.
        """
        self.system_instructions = """
You are a playlist generator. You output a list of song titles and artists based on the user's prompt. Use the format "song title" - "artist name". Only output real songs. No commentary, no extra words. Here's the prompt for the playlist:
"""

        self.json_instructions = """
Rewrite the following playlist in valid JSON only - no commentary or extra text. Keys should be "title" and "artist". The entire output must be an array of objects, each object containing the keys and the coresponding values. No other keys are allowed. Here's the playlist:
"""

    def get_response(self, prompt, model):
        """
        Runs Ollama with the specified model and prompt. Returns the model's text output as a string.

        Args:
            prompt (str): The users prompt
            model (str): The name or identifier of the Ollama model to use. 

        Returns:
            str: The text output from Ollama, stripped of trailing whitespace. 

        Raises:
            subprocess.CalledProcessError If the 'ollama run' command fails.
        """

        full_prompt = self.system_instructions + prompt

        cmd = [
            "ollama", "run",
            model, full_prompt
        ]

        process = subprocess.run(cmd, capture_output=True, text=True, check=True)

        return process.stdout.strip()
    
    def rewrite_json(self, text, model):
        full_text = self.json_instructions + text

        cmd= [
            "ollama", "run",
            model, full_text
        ]

        process = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return process.stdout.strip()
