from get_embedding import openai_ef
import pandas as pd
import chromadb
from time import sleep

df = pd.read_csv('../csvs/kaggle_datasets_for_chroma.csv')
df.sort_values('TotalDownloads',ascending=False)
df = df.head(30_000)

# (to avoid rate limits)
subsets = [df[i:i+1500] for i in range(0, df.shape[0], 1500)]

client = chromadb.PersistentClient(path="../db")

collection = client.get_or_create_collection("kaggle",
                                             embedding_function=openai_ef,
                                             metadata={"hnsw:space": "cosine"})

metadata = ['Title','Subtitle','TotalVotes','TotalDownloads','TotalUncompressedBytes']
for subset in subsets:

    vector_metadata = subset[metadata].to_dict(orient='records')
    collection.add(
        documents= list(subset['dataset_description']),
        ids= list(subset['DatasetId'].astype(str)),
        metadatas=vector_metadata
    )
    sleep(60)

