from interface.get_embedding import openai_ef
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

if __name__ == "__main__":
    data_descr_collection, user_query_collection = get_kaggle_collections()
    print(data_descr_collection.count())
    print(user_query_collection.count())