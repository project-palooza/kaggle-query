import openai
import chromadb.utils.embedding_functions as embedding_functions
from dotenv import load_dotenv,find_dotenv
import os

_ = load_dotenv(find_dotenv())
api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = api_key

# directly from oai
def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    response = openai.Embedding.create(input=[text], model=model)

    return response.data[0].embedding

# from oai via chroma
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=api_key,
                model_name="text-embedding-3-small"
            )