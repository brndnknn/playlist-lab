from openai import OpenAI


class OpenAIManager:
    def __init__(self, api_key, model='gpt-4.1-nano', temperature=0.7):
        self.model = model
        self.temperature = temperature
        self.client = OpenAI(api_key = api_key)
        self.system_prompt = (
            "You are an AI DJ. Given a creative theme or scenario, return a playlist "
            "as a JSON array of objects with 'title' and 'artist' keys."
        )

    def get_response(self, prompt):

        response = self.client.responses.create(
            model=self.model,
            temperature=self.temperature,
            instructions=self.system_prompt,
            input=prompt
        )
        return response.output_text