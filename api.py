#%%
import json
import requests
from bs4 import BeautifulSoup
import random

def get_character_list():
    # URL of the page to scrape
    url = "https://www.prydwen.gg/afk-journey/characters"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the page content
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find all character names after "/" of the `<a href="/afk-journey/characters/[NAME]">` under the `<div class="avatar-card card">`. There are around 62 characters for now.
        character_list = [a["href"].split("/")[-1] for a in soup.select("div.avatar-card.card a[href^='/afk-journey/characters/']")]

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    return character_list

def get_character_info(character_name: str, save_to_file: bool = False):
    # URL of the page to scrape
    url = f"https://www.prydwen.gg/afk-journey/characters/{character_name}"

    # Send a GET request to the URL
    response = requests.get(url)
    
    # debug
    with open("response.tmp", "w", encoding="utf-8") as file:
        file.write(response.text)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the page content
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the desired <div> section
        content_div = soup.find("div", class_="content afk")
        
        if content_div:
            if save_to_file:
                # Save the content to a .txt file
                with open("character_info.tmp", "w", encoding="utf-8") as file:
                    file.write(str(content_div))
                print("Content saved to 'character_info.tmp'.")
            return str(content_div)
        else:
            print("The specified <div> was not found.")
            return None
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

def extract_character_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract character name
    character_name = soup.select_one('h1 > strong.faction').text.strip()

    # Extract faction
    faction = soup.select_one('h1 > strong.faction').get('class')[1].strip()

    # Extract class
    character_class = soup.select_one('h2 > strong:nth-of-type(2)').text.strip()

    # Extract level
    level = soup.select_one('h2 > strong').text.strip()

    # Extract attack range
    attack_range = soup.select_one('h2 > strong:nth-of-type(3)').text.strip()

    # Extract introduction
    introduction = ' '.join(p.text.strip() for p in soup.select('.character-intro .char-intro p'))

    # Extract skills
    skills = []
    skill_sections = soup.select('.skills .col')
    for skill_section in skill_sections:
        skill = {
            "name": skill_section.select_one('.skill-name').text.strip(),
            "type": skill_section.select_one('.skill-type').text.strip(),
            "description": skill_section.select_one('.skill-description p').text.strip(),
            "additional_info": {info.select_one('span').text.strip(): info.text.split(":")[-1].strip()
                                for info in skill_section.select('.additional-information p')},
            "upgrades": [upgrade.text.strip() for upgrade in skill_section.select('.skill-upgrades p')]
        }
        skills.append(skill)

    # Extract review
    review = ' '.join(p.text.strip() for p in soup.select('.review.raw p'))

    # Extract pros
    pros = [li.text.strip() for li in soup.select('.pros .list ul li')]

    # Extract cons
    cons = [li.text.strip() for li in soup.select('.cons .list ul li')]

    # Extract ratings
    ratings = {
        "general": {rating.select_one('p').text.strip(): rating.select_one('.rating-box').text.strip()
                    for rating in soup.select('.detailed-ratings.general .rating-box-container')},
        "dream": {rating.select_one('p').text.strip(): rating.select_one('.rating-box').text.strip()
                  for rating in soup.select('.detailed-ratings.dream .rating-box-container')}
    }

    # Compile results
    character_info = {
        "name": character_name,
        "faction": faction,
        "class": character_class,
        "level": level,
        "attack_range": attack_range,
        "introduction": introduction,
        "skills": skills,
        "review": review,
        "pros": pros,
        "cons": cons,
        "ratings": ratings
    }

    # enumerate all items in the character_info dictionary including nested lists and dictionaries. 
    # For each string value:
    # 1. replace '\n' with ' '
    # 2. make sure there are no ' ' char repeated more than once.

    for key, value in character_info.items():
        if isinstance(value, str):
            character_info[key] = ' '.join(value.split())
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, str):
                    character_info[key][i] = ' '.join(item.split())
                elif isinstance(item, dict):
                    for k, v in item.items():
                        if isinstance(v, str):
                            character_info[key][i][k] = ' '.join(v.split())
                        elif isinstance(v, list):
                            for j, subitem in enumerate(v):
                                if isinstance(subitem, str):
                                    character_info[key][i][k][j] = ' '.join(subitem.split())
    
    return character_info

#%%
# Example usage

if __name__ == "__main__":
    # Get the character list
    char_list = get_character_list()
    print(char_list)

    # Get the character info
    random_character = random.choice(char_list)
    char_info = get_character_info(random_character)

    # Extract the character info
    if char_info:
        character_info = extract_character_info(char_info)
        # save to character_info.json
        with open('character_info.json', 'w') as file:
            json.dump(character_info, file) #, indent=4)

# %%
