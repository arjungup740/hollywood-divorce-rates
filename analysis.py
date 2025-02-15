import os
import pandas as pd
import pickle
import numpy as np
import re
pd.set_option('display.max_colwidth', 1000)

filename = 'list_of_dicts.pkl'
with open(filename, 'rb') as file:
    list_of_dicts = pickle.load(file) 

raw = pd.DataFrame(list_of_dicts)
list(raw.columns)

all_relationship_terms = [
    'Spouses',
    'Spouse',
    'Spouse(s)',
    'Partners',
    'Partner',
    'Partner(s)',
]

spouse_terms = [
    'Spouses',
    'Spouse',
    'Spouse(s)',
]

children_terms = [
    'Children',
    'Parent',
    'Parents',
    'Mother',
    'Father',
    'Parent(s)',
    'Children',
]


filtered_data = [
    {
        k: v.replace('\u200b', '') if k in all_relationship_terms else v
        for k, v in entry.items() if k in ['actor'] + all_relationship_terms
    }
    for entry in list_of_dicts
] # add this to replace \xa0

# Define the regex pattern to match each marriage/partnership
pattern = re.compile(r'([a-zA-Z\s]+\(.*?\))')

# Initialize an empty list to store the rows
rows = []

# Iterate through each entry in the filtered_data
for entry in filtered_data:
    actor = entry['actor']
    for key in all_relationship_terms:
        if key in entry:
            # Find all matches for the current relationship term (Spouses, Partners, etc.)
            matches = pattern.findall(entry[key])
            for match in matches:
                rows.append({
                    'actor': actor,
                    'variable': key,
                    'value': match.strip()  # Strip any leading/trailing whitespace
                })

# Create the DataFrame from the rows
df = pd.DataFrame(rows, columns=['actor', 'variable', 'value'])

## extract names & the details
df[['name', 'details']] = df['value'].str.extract(r'([a-zA-Z\s]+)\s*(\(.*?\))').apply(lambda x: x.str.strip())
pattern = re.compile(r'([a-zA-Z]+\.? \d{4})\s* *;? *\s*([a-zA-Z]+\.? \d{4})?') #re.compile(r'([a-zA-Z]{1,4}\.\s*\d{4})(?:;\s*([a-zA-Z]{1,4}\.\s*\d{4}))?')

## Apply the regex to extract the matches into two columns
df[['first_event', 'second_event']] = df['details'].str.extract(pattern)
df

## get out the m. and the year
df['first_abbrev'] = df['first_event'].str.extract(r'(\w+)\.? ')
df['second_abbrev'] = df['second_event'].str.extract(r'(\w+)\.? ')
## if your marriage makes it, then give the np.nan a "surv" for survived
df.loc[ (df.variable.isin(spouse_terms)) &  (df['second_abbrev'].isnull()), 'second_abbrev'] = 'surv'

######## QA + digging into regexes
## check how many don't have semi-colons in them
len(df[df['variable'].isin(spouse_terms)])
df[df['variable'].isin(spouse_terms)].isnull().sum()
## can add a check to see how many have two sets of numbers indicating two events

df[(df['variable'].isin(spouse_terms)) & (df['first_event'].notnull())]['first_event'].unique()

# come back and address
df[(df['variable'].isin(spouse_terms)) & (df['first_event'].isnull())][['value', 'first_event']]
df[(df['variable'].isin(spouse_terms)) & (df['second_event'].isnull())][['value', 'second_event']]
df[(df['variable'].isin(spouse_terms)) & (df['second_event'].isnull())]['value'].unique()

## looking at abbrevs
df['first_abbrev'].unique()
len(df[ ( df['variable'].isin(spouse_terms) ) & ~( df['first_abbrev'].isin(['m']) ) ]) # not too bad

df['second_abbrev'].unique()
df[ ( df['variable'].isin(spouse_terms) ) & ( df['second_abbrev'].isnull())  ].details.unique()

######## Make some charts

working = df[df['variable'].isin(spouse_terms)]
len(working) # 1452 marriages

## 1) count of marriages
count_table = working.groupby('actor')['first_abbrev'].count().reset_index().rename(columns = {'first_abbrev':'count'})

len(count_table[count_table['count'] != 1]) # have been divorced
# add who have been divorced and only one marriage
len(count_table[count_table['count'] == 1])

working.groupby(['first_abbrev', 'second_abbrev'])['actor'].agg(['count', 'nunique'])#.sum()

working.groupby('actor')

div_abbrevs = ['ann', 'annul', 'div', 'sep']


## 2) number more than one


########### Trying the straight df way

df = raw[['actor', 'Born'] + spouse_terms]
# df['Born'][0]
df.loc[:,'num_categories'] = len(spouse_terms) - df[spouse_terms].isnull().sum(axis=1)
df[df['num_categories'] == 1]
df[spouse_terms] = df[spouse_terms].replace(np.nan, None)

df[df['Spouse(s)'].notnull()] # only 5 people, so we fine

df['Spouses'][0]

df[df['Spouses'].notnull()][['Spouses']].iloc[0]


def analyze_marriages(spouse_info):
    # Check if the spouse_info is None or an empty string
    if not spouse_info:
        return pd.Series({
            'num_marriages': 0,
            'marriage_status': [],
            'marriage_durations': []
        })
    
    # Regular expression to match marriage information
    # This regex now captures any 1-4 letter abbreviations, with or without a period, followed by an optional year
    marriage_pattern = re.compile(r'\(\s*m\. (\d{4})\s*;.*?([a-zA-Z]{1,4}\.?)?\s*(\d{4})?\s*\)')
    
    # Find all matches
    marriages = marriage_pattern.findall(spouse_info)
    
    num_marriages = len(marriages)
    marriage_durations = []
    marriage_status = []
    
    for marriage in marriages:
        start_year = int(marriage[0])
        end_year = int(marriage[2]) if marriage[2] else None
        status = marriage[1] if marriage[1] else 'still married'  # Assume still married if no status provided
        
        if end_year:
            duration = end_year - start_year
        else:
            duration = None  # Duration is None if still married
        
        marriage_durations.append(duration)
        marriage_status.append(status)
    
    return pd.Series({
        'num_marriages': num_marriages,
        'marriage_status': marriage_status,
        'marriage_durations': marriage_durations
    })

# Apply the function to the "Spouses" column, handling None values
df[['num_marriages', 'marriage_status', 'marriage_durations']] = df['Spouses'].apply(analyze_marriages)


df[df['actor'] == 'Marlon Brando']['Spouses']

analyze_marriages(df['Spouses'][0])

# Display the updated DataFrame
print(df.head())


###### extract the spouse information. 

# Extracting specific information like Spouses or Partner
spouses_or_partners = infobox_data.get('Spouses', None)

print(f"Spouses/Partner: {spouses_or_partners}")
print("Full Infobox Data:")
for key, value in infobox_data.items():
    print(f"{key}: {value}")


# Actor, Born, variable, value
# robert deniro, date, marriage 1, 'Diahnne Abbott \u200b \u200b ( m. 1976; div. 1988) \u200b
# robert deniro, date, marriage 2, 'Grace Hightower \u200b \u200b ( m. 1997; sep. 2018) \u200b'
# Marlon Brando, etc...