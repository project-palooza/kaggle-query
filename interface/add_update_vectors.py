from get_collections import get_kaggle_collections
import pandas as pd
from time import sleep

df = pd.read_csv('../csvs/kaggle_datasets_for_chroma.csv')
df.sort_values('TotalDownloads',ascending=False)
df = df.head(30_000)

# (to avoid rate limits)
subsets = [df[i:i+1500] for i in range(0, df.shape[0], 1500)]

collection, _ = get_kaggle_collections()

metadata = ['Title','Subtitle','TotalVotes','TotalDownloads','TotalUncompressedBytes']
for subset in subsets:

    vector_metadata = subset[metadata].to_dict(orient='records')
    collection.add(
        documents= list(subset['dataset_description']),
        ids= list(subset['DatasetId'].astype(str)),
        metadatas=vector_metadata
    )
    sleep(60)

