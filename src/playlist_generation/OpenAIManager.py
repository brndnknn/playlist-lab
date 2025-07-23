"""
Handles interaction with the OpenAI API for playlist generation.

Provides methods for generating playlist text from prompts and for converting
freeform playlist output into JSON using an LLM.
"""

from openai import OpenAI


class OpenAIManager:
    def __init__(self, api_key, model='gpt-4.1-nano', temperature=0.8):
        """
        Initializes the OpenAIManager with API key, model, and temperature.

        Args:
            api_key (str): OpenAI API key.
            model (str, optional): Model name to use for completions. Defaults to 'gpt-4.1-nano'.
            temperature (float, optional): Sampling temperature. Defaults to 0.8.
        """
        self.model = model
        self.temperature = temperature
        self.client = OpenAI(api_key = api_key)
        self.system_prompt = (
            "You are an AI DJ. Given a creative theme or scenario, "
            "return a playlist of only real songs, with each song "
            "having a title and an artist."
        )
        self.alt_sys_prompt = (
                "Convert the given playlist of songs into a list in JSON format. "
                "Each item should be an object with keys 'title' and 'artist'. "
                "Only include songs contained in the prompt."
            )

    def get_response(self, prompt, model_name=None):
        """
        Sends a playlist prompt to the OpenAI model and returns the freeform text response.

        Args:
            prompt (str): The user's playlist prompt.
            model_name (str, optional): Model name to override default. Defaults to None.

        Returns:
            tuple: (str output_text, object usage) where output_text is the LLM response,
                and usage contains token info.
        """
        model = model_name if model_name is not None else self.model
        response = self.client.responses.create(
            model=model,
            temperature=self.temperature,
            instructions=self.system_prompt,
            input=prompt
        )

        return response.output_text, response.usage

    def convert_to_json(self, prompt):
        """
        Converts a freeform playlist text into structured JSON using the OpenAI model.

        Args:
            prompt (str): The playlist text to convert.

        Returns:
            str: JSON-formatted playlist as output by the LLM.
        """
        response = self.client.responses.create(
            model=self.model,
            temperature=self.temperature,
            instructions=self.alt_sys_prompt,
            input=prompt
        )

        return response.output_text