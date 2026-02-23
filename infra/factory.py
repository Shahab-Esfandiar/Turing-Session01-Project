# infra/factory.py
import os
from dotenv import load_dotenv
from infra.client import OpenAIClient
from core.exceptions import LLMServiceError

load_dotenv()

class ClientFactory:
    """Factory to handle AI provider switching."""
    @staticmethod
    def get_client(provider_name, model_name=None):
        provider = provider_name.lower()
        
        if provider == "openai":
            api_key = os.getenv("API_KEY")
            base_url = os.getenv("BASE_URL")
            # Defaults to ENV model if no specific model is passed
            model = os.getenv("MODEL_NAME", "gpt-4o")
            return OpenAIClient(api_key, base_url, model)
        
        elif provider == "ollama":
            import ollama
            class OllamaClient:
                def __init__(self, m_name):
                    self.m_name = m_name or "gemma3:4b"
                def predict(self, prompt):
                    res = ollama.chat(model=self.m_name, messages=[{"role": "user", "content": prompt}])
                    return res['message']['content']
            return OllamaClient(model_name)
            
        raise LLMServiceError(f"Provider '{provider_name}' is not supported.")