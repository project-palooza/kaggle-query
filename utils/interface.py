from .get_collections import get_kaggle_collections
import pandas as pd
import uuid

data_descr_collection, user_query_collection = get_kaggle_collections()

def assign_query_id():
    return uuid.uuid4().int & (1<<32)-1

def embed_user_query(query):
    query_id = assign_query_id()
    user_query_collection.add(ids=[str(query_id)], documents=[query])
    query_embedding = user_query_collection.get(ids=[str(query_id)],include=["embeddings"])['embeddings']
    
    return query_embedding

def find_datasets(query_embedding):
    query_response = \
    data_descr_collection.query(
    query_embeddings=query_embedding,
    n_results=5
    )

    metadata = query_response['metadatas'][0]
    descriptions = query_response['documents'][0]
    
    return descriptions, metadata

def reply_to_user(metadata):
    metadata_df = pd.DataFrame(metadata).sort_values('TotalDownloads',ascending=False).reset_index(drop = True)

    print("here's what I found:\n")
    for index,row in metadata_df.iterrows():    
        print(f"{index + 1}. {row['Title']}{row['Subtitle']} -- total downloads: {row['TotalDownloads']}")

    print("\ninterested in any of these?")

def interface(query):
    embedding = embed_user_query(query)
    _, metadata = find_datasets(embedding)
    reply = reply_to_user(metadata)
    print(reply)
    return reply

if __name__ == "__main__":
    import sys
    cmd_line_qry = sys.argv[1]
    interface(cmd_line_qry)