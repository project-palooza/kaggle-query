import pandas as pd
import tiktoken

def filter_long_descriptions(df,embedding_encoding = "cl100k_base",max_tokens = 8191):
    
    encoding = tiktoken.get_encoding(embedding_encoding)
    df["n_tokens"] = df['dataset_description'].apply(lambda x: len(encoding.encode(x)))
    df = df[df.n_tokens <= max_tokens]
    return df

def kaggle_datasets_for_chroma(cost_per_million_tokens = .02):

    # title, subtitle, size, description
    df = pd.read_csv('/Users/arad/repos/pp_kaggle_query/csvs/DatasetVersions.csv')
    df = df.loc[~df['Description'].isna(),]
    df['CreationDate'] = pd.to_datetime(df['CreationDate'])
    df.sort_values(by = 'CreationDate',inplace = True,ascending = False)
    df.drop_duplicates(subset = 'DatasetId',keep = 'first',inplace = True)
    keep_columns = ['DatasetId','CreatorUserId','Description','Title','Subtitle','Slug','TotalUncompressedBytes']
    df = df[keep_columns]

    # votes, downloads, file type
    ddf = pd.read_csv('/Users/arad/repos/pp_kaggle_query/csvs/Datasets.csv')
    ddf = ddf[['Id','TotalVotes','TotalDownloads']]

    df = pd.merge(df,ddf,left_on = 'DatasetId',right_on = 'Id',how = 'left')

    # tags
    tddf = pd.read_csv('/Users/arad/repos/pp_kaggle_query/csvs/DatasetTags.csv')
    tdf = pd.read_csv('/Users/arad/repos/pp_kaggle_query/csvs/Tags.csv')

    tddf = pd.merge(tddf,tdf,left_on='TagId',right_on = 'Id')
    tddf.loc[tddf['Description'].isna(),'Description'] = ''
    tddf['TagDescriptions'] = tddf['Name'] + ":" + tddf['Description']
    tddf_grouped = tddf.groupby('DatasetId')['TagDescriptions'].apply(list).reset_index()

    df = pd.merge(df,tddf_grouped,on = 'DatasetId',how = 'left')

    df['dataset_description'] = df.apply(lambda row: f"Title: {row['Title']} Subtitle: {row['Subtitle']} Description: {row['Description']} Tags: {row['TagDescriptions']}", axis=1)

    df = filter_long_descriptions(df)

    df.to_csv('/Users/arad/repos/pp_kaggle_query/csvs/kaggle_datasets_for_chroma.csv',index = False)

    print(f"total cost to embed: ${(df['n_tokens'].sum()/1_000_000)*cost_per_million_tokens}")

    return df

if __name__ == "__main__":
    kaggle_datasets_for_chroma()