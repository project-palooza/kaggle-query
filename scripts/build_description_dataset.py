import pandas as pd
from soupify_and_extract_description import soupify_and_extract_description

# assume kaggle meta data already exists 

kaggle_df = pd.read_csv('../csvs/dataset_df.csv')

list_of_descriptions = [] # list of dicts

for _,row in kaggle_df.iterrows():
    try:
        description = soupify_and_extract_description(row['url']) # dict
        print(f"added {description["description"]} to the list")
        list_of_descriptions.append(description)
    except Exception as e:
        print(f"whoops\n{e.message}")


description_df = pd.DataFrame(list_of_descriptions)
descriptions_found = description_df.shape[0]
mask = (description_df['description'] == "not found") & (description_df['name'] == "not found")
descriptions_not_found = description_df.loc[mask].shape[0]
print(f"{descriptions_found} descriptions\n")
print(f"{round(descriptions_not_found/descriptions_found,3)*100}% missing")


