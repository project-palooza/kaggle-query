import sys
import json
import requests
from bs4 import BeautifulSoup

dataset_url = sys.argv[1] # this let's us give the script a url as input from the command line

response = requests.get(dataset_url)

if response.status_code == 200:
    print("it worked")
    soup = BeautifulSoup(response.text,'html.parser')
else:
    print("didn't work")
    print(f"response status: {response.status_code}")

script_tag = soup.find('script', {'type': 'application/ld+json'})

if script_tag:
    json_data = json.loads(script_tag.string)

    description = json_data.get('description', '')
    name = json_data.get('name', '')

    print(description)
    print(name)
else:
    print("Script tag not found.")