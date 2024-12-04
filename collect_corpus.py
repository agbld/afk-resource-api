#%%
# Import libraries
from api import get_character_list, get_character_info, extract_character_info
import json
import os
from tqdm import tqdm

#%%
# Get character list
characters = get_character_list()

#%%
# Get and save character info

if not os.path.exists('./data'):
    os.makedirs('./data')

for character in tqdm(characters, desc="Collecting character info"):
    info_html = get_character_info(character)
    info = extract_character_info(info_html)
    with open(f'./data/{character}.json', 'w') as file:
        json.dump(info, file)

#%%