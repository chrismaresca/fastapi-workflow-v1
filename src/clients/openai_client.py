from openai import OpenAI
from src.utils.config import settings

openai_client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
)

