import wikipediaapi
import openai
from dotenv import load_dotenv
import os
import pandas as pd
load_dotenv(dotenv_path='.env')

actor_df = pd.read_csv('new_actor_stuff/1000_actors_input.csv')
actor_df['name'] = actor_df['document_url'].str.split('/').str[-1].str.replace('_', ' ')
actor_df

## initialize wiki object
wiki_wiki = wikipediaapi.Wikipedia(
    user_agent='MyProjectName (merlin@example.com)',
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI
)

