from openai import OpenAI


class OpenAIManager:
    def __init__(self, api_key, model='gpt-4.1-nano', temperature=0.8):
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
        model = model_name if model_name is not None else self.model
        response = self.client.responses.create(
            model=model,
            temperature=self.temperature,
            instructions=self.system_prompt,
            input=prompt
        )

        return response.output_text, response.usage

    def convert_to_json(self, prompt):

        response = self.client.responses.create(
            model=self.model,
            temperature=self.temperature,
            instructions=self.alt_sys_prompt,
            input=prompt
        )

        return response.output_text