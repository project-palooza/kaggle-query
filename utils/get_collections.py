from get_embedding import openai_ef
import chromadb

client = chromadb.PersistentClient(path="../db")

def get_kaggle_collections():
    data_descr_collection = client.get_or_create_collection("kaggle",
                                             embedding_function=openai_ef,
                                             metadata={"hnsw:space": "cosine"})
    user_query_collection = client.get_or_create_collection("user",
                                             embedding_function=openai_ef,
                                             metadata={"hnsw:space": "cosine"})
    return data_descr_collection, user_query_collection

