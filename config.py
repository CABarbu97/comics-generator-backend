import os

class Config:
    REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
