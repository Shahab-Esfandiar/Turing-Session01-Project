# app/llm_json_service.py
import json
import re
from core.logger import logger

class LLMJsonEngine:
    def __init__(self, llm_client):
        self.client = llm_client

    def generate(self, df, template):
        # Generate stats and sample
        summary_stats = df.describe(include='all').to_json(force_ascii=False)
        data_sample = df.head(15).to_json(orient='records', force_ascii=False)
        
        prompt = template.format(
            columns=", ".join(df.columns),
            stats=summary_stats,
            data=data_sample
        )
        
        raw_response = self.client.predict(prompt)
        logger.debug(f"Raw LLM Response: {raw_response[:100]}...")
        
        return self._clean_json_response(raw_response)

    def _clean_json_response(self, response_text):
        """Extracts JSON content from Markdown or dirty strings."""
        # 1. Try to find content inside Markdown code blocks
        code_block_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", response_text)
        if code_block_match:
            return code_block_match.group(1).strip()
        
        # 2. Try to find the first '{' and last '}'
        start = response_text.find('{')
        end = response_text.rfind('}')
        if start != -1 and end != -1:
            return response_text[start:end+1].strip()
            
        # 3. Last resort: just strip whitespace
        return response_text.strip()