# infra/client.py
from openai import OpenAI
import time

class BaseLLMClient:
    """Abstract base for all LLM providers."""
    def predict(self, prompt: str) -> str:
        raise NotImplementedError

class OpenAIClient(BaseLLMClient):
    """Client for OpenAI compatible APIs."""
    def __init__(self, api_key, base_url, model_name):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model_name = model_name

    def predict(self, prompt: str, retries=3, delay=2) -> str:
        for attempt in range(1, retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                if attempt == retries:
                    raise e
                time.sleep(delay)