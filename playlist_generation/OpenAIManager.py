from openai import OpenAI


class OpenAIManager:
    def __init__(self, api_key, model='gpt-4.1-nano', temperature=0.8):
        self.model = model
        self.temperature = temperature
        self.client = OpenAI(api_key = api_key)
        self.system_prompt = (
            "You are an AI DJ. Given a creative theme or scenario, "
            "return a playlist of only real songs in JSON format "
            "with each song having a title and an artist."
        )

    def get_response(self, prompt, model_name=None):
        model = model_name if model_name is not None else self.model
        response = self.client.responses.create(
            model=model,
            temperature=self.temperature,
            instructions=self.system_prompt,
            input=prompt
        )

        print(response.model)
        return response.output_text