#%%
import requests
from bs4 import BeautifulSoup
import random

def get_character_info(character_name: str):
    # URL of the page to scrape
    url = f"https://www.prydwen.gg/afk-journey/characters/{character_name}"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the page content
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the desired <div> section
        content_div = soup.find("div", class_="content afk")
        
        if content_div:
            # Save the content to a .txt file
            with open("character_info.tmp", "w", encoding="utf-8") as file:
                file.write(content_div.get_text(strip=True))
            print("Content saved to 'character_info.tmp'.")
        else:
            print("The specified <div> was not found.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    return content_div.get_text(strip=True)

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

#%%
# Example usage

if __name__ == "__main__":
    # Get the character list
    char_list = get_character_list()
    print(char_list)

    # Get the character info
    random_character = random.choice(char_list)
    char_info = get_character_info(random_character)

# %%
