import os
import requests
from dotenv import load_dotenv
from loguru import logger

class llm_api_call:
    def __init__(self, google_api_key=None, model_name="models/gemini-2.0-flash"):
        """
        Initializes the Gemini API client.
        If no API key is provided, it will be auto-loaded from the .env file or environment.
        """
        logger.info(f"Initializing llm_api_call with model: {model_name}")
        self.model = model_name
        self.api_key = google_api_key  # May be None initially

    def _load_api_key(self):
        """Ensures the API key is loaded from .env or environment."""
        logger.info("Loading API key.")
        # Load .env silently each time to catch any updated keys
        load_dotenv(override=False)

        if not self.api_key:
            self.api_key = os.getenv("GOOGLE_API_KEY")

        if not self.api_key:
            logger.error("Google API key not found.")
            raise ValueError("Google API key not found. Please set GOOGLE_API_KEY in .env or environment.")
        logger.info("API key loaded successfully.")

    def generate(self, prompt: str) -> str:
        """
        Calls Google Gemini API to generate a response for the given prompt.
        Automatically loads API key if not already available.
        """
        logger.info("Generating response from LLM.")
        try:
            # Ensure key is loaded before making request
            self._load_api_key()

            url = f"https://generativelanguage.googleapis.com/v1/{self.model}:generateContent"
            headers = {"Content-Type": "application/json"}
            params = {"key": self.api_key}
            data = {
                "contents": [
                    {"parts": [{"text": prompt}]}
                ]
            }

            response = requests.post(url, headers=headers, params=params, json=data)

            if response.ok:
                logger.info("Successfully received response from LLM.")
                resp_json = response.json()
                candidates = resp_json.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
                return "No response text found."
            else:
                logger.error(f"Error from LLM API: {response.status_code} {response.text}")
                return f"Error: {response.status_code} {response.text}"

        except Exception as e:
            logger.error(f"Exception occurred during LLM call: {e}")
            return f"Exception occurred: {str(e)}"


# Example usage:
# llm = llm_api_call()
# answer = llm.generate("Who won the FIFA World Cup in 2018?")
# print(answer)
