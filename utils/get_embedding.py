import openai
from dotenv import load_dotenv,find_dotenv
import os

_ = load_dotenv(find_dotenv())
api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = api_key

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    response = openai.Embedding.create(input=[text], model=model)

    return response.data[0].embedding