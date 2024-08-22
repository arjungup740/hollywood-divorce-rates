import wikipediaapi
import openai
from dotenv import load_dotenv
import os
import pandas as pd
load_dotenv(dotenv_path='.env')

## initialize wiki object
wiki_wiki = wikipediaapi.Wikipedia(
    user_agent='MyProjectName (merlin@example.com)',
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI
)

# Assuming you have your API key stored in the OPENAI_API_KEY environment variable
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def check_substance_abuse(actor, text):
    prompt = f"Based on the following text about {actor}, do they struggle or have they ever struggled with alcoholism, drug use, or other substance abuse issues? Provide a clear answer with reasoning. Text: '''{text}'''"
    
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert in identifying substance abuse issues in written descriptions."},
            {"role": "system", "content": 
                    """Return the answer as a dictionary where the key is the type of drug of alcohol, a 1 if the person did indeed abuse it, a 0 if they didn't or you are not sure. 
                        Add a key of 'reasoning' where the value is text describing your thought process.
                        if the text does not provide  explicit mention of the actor personally having struggled with these issues, you must put 0."""
                },
            {"role": "user", "content": prompt}
        ],
        model="gpt-4o",
    )

    return chat_completion#['choices'][0]['message']['content']

# Example usage
p_wiki = wiki_wiki.page("Daniel Radcliffe")
# p_wiki = wiki_wiki.page("Meryl Streep")
result = check_substance_abuse("Daniel Radcliffe",p_wiki.text)
# eval(result.choices[0].message.content)

actor_df = pd.read_csv('new_actor_stuff/1000_actors_input.csv')
actor_df['name'] = actor_df['document_url'].str.split('/').str[-1].str.replace('_', ' ')
actor_df

list_of_dicts = []
error_dicts = []
for actor in actor_df['name']:
    try:
        print(f'processing {actor}')
        p_wiki = wiki_wiki.page(actor)
        result = check_substance_abuse(actor, p_wiki.text)
        list_of_dicts.append(result) # eval(result.choices[0].message.content)
    except Exception as e:
        print(f'hit error {e} on {actor}')
        error_dicts.append({actor:e})
        print(f'result was: {result}\n')

#### coalesce into df

extracted_jsons = []
import json
for completion in list_of_dicts[0:3]:
    # Access the content of the message
    content = completion.choices[0].message.content
    
    # Extract the JSON string from the content
    json_str = content.strip('```python\n```json\n```').strip()
    
    # Parse the JSON string into a dictionary
    json_dict = json.loads(json_str)
    
    # Add the dictionary to the list
    # extracted_jsons.append(pd.Series(json_dict))
    extracted_jsons.append(json_dict)

pd.DataFrame(extracted_jsons)
### one off:
actor = 'Jack Nicholson'
p_wiki = wiki_wiki.page(actor)
result = check_substance_abuse(actor, p_wiki.text)
result.choices[0].message.content