import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from time import sleep

api = KaggleApi()
api.authenticate()

def get_dataset_metadata():


    page_is_valid = True
    page_number = 1
    list_of_dataframes = []

    while page_is_valid:

        sleep(2)

        try:
            datasets = api.dataset_list(page=page_number)
            print(f"successfully pulled data from page {page_number}")
            dataset_list = []

            for dataset in datasets:
                dataset_attributes = vars(dataset)
                dataset_list.append(dataset_attributes)

            dataset_df = pd.DataFrame(dataset_list)
            list_of_dataframes.append(dataset_df)

            page_number += 1
            
        except:
            print(f"failed to pull data from page {page_number}")
            page_is_valid = False


    final_df = pd.concat(list_of_dataframes)

    final_df.to_csv('../csvs/dataset_df.csv',index = False)
    print("dataset_df is ready")

if __name__ == "__main__":
    get_dataset_metadata()

