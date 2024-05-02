import requests
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def get_plants_by_common_name(common_name, auth_token):
    url = "https://trefle.io/api/v1/plants"
    params = {
        "filter[common_name]": common_name,
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
        print("Scientific Name:", plant.get("scientific_name", "N/A"))
        print("Image URL:", plant.get("image_url", "N/A"))
        print()

if __name__ == "__main__":
    common_name = "Lavender"
    plant_data = get_plants_by_common_name(common_name, os.getenv("AUTH_TOKEN"))
    if plant_data:
        print_plant_info(plant_data)
    else:
        print("Failed to fetch plant data.")
