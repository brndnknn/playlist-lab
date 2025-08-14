"""
Handles interaction with the OpenAI API for playlist generation.

Provides methods for generating playlist text from prompts and for converting
freeform playlist output into JSON using an LLM.
"""

from openai import OpenAI


class OpenAIManager:
    def __init__(self, api_key, model='gpt-5-nano'):
        """
        Initializes the OpenAIManager with API key, model, and temperature.

        Args:
            api_key (str): OpenAI API key.
            model (str, optional): Model name to use for completions. Defaults to 'gpt-4.1-nano'.
            temperature (float, optional): Sampling temperature. Defaults to 0.8.
        """
        self.model = model
        self.client = OpenAI(api_key = api_key)
        self.system_prompt = (
            """You are an AI DJ with a mischievous sense of humor and impeccable taste in music.
                Your job is to create playlists in response to surreal, whimsical, or unusual prompts.

                Rules:

                Output 20–30 songs, one per line, in the format:
                Song Title — Artist

                Only include real, verifiable songs (no invented titles or fake artists).

                Do not include more than two songs by the same artist.

                Keep the playlist coherent — it should feel intentional and unified.

                Infuse the playlist with quirky, funny, punny, and creative choices that cleverly reference the prompt.

                Balance thematic alignment (lyrics, titles, or artist names connected to the prompt) with musical flow (songs that could believably exist together in one playlist).

                Do not include explanations, commentary, numbering, or extra prose. Output only the playlist text.


                Goal:
                Make the playlist surprising, witty, and cohesive — something that feels like a joke, a story, and a genuinely listenable set of songs all at once.
                """
                    # "Create a playlist of 20–30 real songs (Title — Artist) that best fits this prompt.\n"
                    # "Rules:\n"
                    # "• Only output the list, one per line, no numbering, no extra prose.\n"
                    # "• Use real, verifiable tracks.\n"
                    # "• Favor clever, funny, punny, and thematic choices.\n\n"
            # "You are an AI DJ. Given a creative theme or scenario, "
            # "return a playlist of only real songs, with each song "
            # "having a title and an artist."
        )
        self.alt_sys_prompt = (
                "Convert the given playlist of songs into a list in JSON format. "
                "Each item should be an object with keys 'title' and 'artist'. "
                "Only include songs contained in the prompt."
            )

    def get_response(self, prompt, model_name=None, effort="minimal", verb="low"):
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
            reasoning={"effort": effort},
            text={"verbosity": verb},
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
            reasoning={"effort": "minimal"},
            text={"verbosity": "low"},
            instructions=self.alt_sys_prompt,
            input=prompt
        )

        return response.output_text