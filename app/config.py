import openai
from dotenv import load_dotenv
import os

print("Config module executed")

def load_configuration():
    """Load environment variables and set up API keys."""
    
    # Load environment variables from .env file
    load_dotenv()

    # Set the API key for OpenAI
    #openai.api_key = os.getenv("OPENAI_API_KEY")
    return os.getenv("OPENAI_API_KEY")