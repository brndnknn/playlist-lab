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
# system
You are a playlist generator. Please output ONLY the list of songs. Each song should have a title in quotes followed by a dash and then the artist name. No extra commentary, disclaimers, or reasoning.

# user

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