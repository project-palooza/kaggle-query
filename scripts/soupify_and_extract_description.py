import sys
import json
import requests
from bs4 import BeautifulSoup

def soupify_and_extract_description(dataset_url):

    """ scrapes kaggle page for dataset description and name
        input: string (dataset_url)
        output: dict {name: .., description: ..} 
    """

    description_d = {"name":"not found","description":"not found"}

    response = requests.get(dataset_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text,'html.parser')
    else:
        print("didn't work!\n")
        print(f"response status: {response.status_code}")

    script_tag = soup.find('script', {'type': 'application/ld+json'})

    if script_tag:
        json_data = json.loads(script_tag.string)

        description_d["name"] = json_data.get('name', '')
        description_d["description"] = json_data.get('description', '')
    else:
        print("script tag not found.\nreturning empty strings")

    return description_d

if __name__ == "__main__":
    dataset_url = sys.argv[1] # this let's us give the script a url as input from the command line
    dataset_name = dataset_url.rsplit("/",1)[-1]
    description_d = soupify_and_extract_description(dataset_url)
    with open(f"{dataset_name}.json","w") as j:
        json.dump(description_d,j)