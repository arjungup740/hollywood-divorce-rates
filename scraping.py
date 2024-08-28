import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import pickle

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

## rescrapes
filename = 'not_in_df.pkl'
with open(filename, 'rb') as file:
    not_in_df = pickle.load(file) 

url_list = actor_df[actor_df['name'].isin(not_in_df)]['document_url']
# url_list = actor_df['document_url']
# Extract the data from the infobox
start = time.time()
list_of_dicts = []
error_list = []
for i, url in enumerate(url_list):
    print(f'Currently scraping {url} which is number {i}')
    try:
        list_of_dicts.append(get_infobox(url))
        time.sleep(1)
    except Exception as e:
        error_list.append({'url':url, 'error':e})
end = time.time()
print(f'took {end - start}')

# Specify the filename for storing the pickled data
# filename = 'list_of_dicts.pkl'
filename = 'missings_dict.pkl'
# Open the file in binary write mode and use pickle.dump to save the list
with open(filename, 'wb') as file:
    pickle.dump(list_of_dicts, file)

for entry in list_of_dicts:
    if entry['actor'] == 'Emma Watson':
        print(entry)


#######

# test = actor_df['document_url'][0:2].apply(get_infobox) # want error handling, otherwise do this next time

url = 'https://en.wikipedia.org/wiki/Marlon_Brando'
infobox_data = get_infobox(url)

spouses_or_partners = infobox_data.get('Spouses', None)

print(f"Spouses/Partner: {spouses_or_partners}")
print("Full Infobox Data:")
for key, value in infobox_data.items():
    print(f"{key}: {value}")