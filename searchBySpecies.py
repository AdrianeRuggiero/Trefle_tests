import requests
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def get_plants_by_species(species, auth_token):
    url = "https://trefle.io/api/v1/plants"
    params = {
        "filter[species]": species,
        "token": auth_token
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print("Error:", response.text)
        return None

def print_plant_info(plants):
    for plant in plants:
        print("Common Name:", plant.get("common_name", "N/A"))
        print("Scientific Name:", plant.get("scientific_name", "N/A"))
        print("Image URL:", plant.get("image_url", "N/A"))
        print()

if __name__ == "__main__":
    species_name = "Cocos nucifera"  # Nome científico da espécie de interesse
    plant_data = get_plants_by_species(species_name, os.getenv("AUTH_TOKEN"))
    if plant_data:
        print_plant_info(plant_data)
    else:
        print("Failed to fetch plant data.")
