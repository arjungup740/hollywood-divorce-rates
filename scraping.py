import wikipediaapi
import openai
from dotenv import load_dotenv
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

load_dotenv(dotenv_path='.env')

# Send a GET request to the URL
def get_infobox(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find the infobox
    infobox = soup.find('table', {'class': 'infobox biography vcard'})

    # Function to extract data from infobox rows
    def extract_infobox_data(url, infobox):
        actor = url.split('/')[-1].replace('_', ' ')
        info = {'actor':actor, 'url':url}
        if infobox:
            rows = infobox.find_all('tr')
            for row in rows:
                header = row.find('th')
                data = row.find('td')
                if header and data:
                    key = header.text.strip()
                    value = data.get_text(separator=' ', strip=True)
                    info[key] = value
        return info
    
    infobox_data = extract_infobox_data(url, infobox)

    return infobox_data

## grab the infoboxes for a bunch of people
actor_df = pd.read_csv('1000_actors_input.csv')
actor_df['name'] = actor_df['document_url'].str.split('/').str[-1].str.replace('_', ' ')
actor_df

# Extract the data from the infobox
start = time.time()
list_of_dicts = []
for url in actor_df['document_url']:
    try:
        list_of_dicts.append(get_infobox(url))
    except Exception as e:
        list_of_dicts.append({'url':url, 'error':e})
end = time.time()
print(f'took {end - start}')

###### extract the spouse informatin

# Extracting specific information like Spouses or Partner
spouses_or_partners = infobox_data.get('Spouses', infobox_data.get('Partner', 'N/A'))

print(f"Spouses/Partner: {spouses_or_partners}")
print("Full Infobox Data:")
for key, value in infobox_data.items():
    print(f"{key}: {value}")


#######

# test = actor_df['document_url'][0:2].apply(get_infobox) # want error handling, otherwise do this next time