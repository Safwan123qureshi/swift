import os
from google import genai
from app.config import settings

class LLMProvider:
    def __init__(self):
        api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable missing.")
        self.client = genai.Client(api_key=api_key)

    def generate_response(self, prompt: str, system_instruction: str, model: str = "gemini-flash-latest") -> str:
        try:
            response = self.client.models.generate_content(
                model=model,
                contents=prompt,
                config={"system_instruction": system_instruction}
            )
            return response.text
        except Exception as e:
            return f"Error generating AI response: {str(e)}"