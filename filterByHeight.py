import requests
import json
from datetime import date
from dotenv import load_dotenv
import os

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()


def get_plants_by_height(average_height, auth_token):
    url = "https://trefle.io/api/v1/species"
    params = {
        "token": auth_token,
        "range[average_height_cm]": average_height
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        plants = response.json().get("data", [])
        filtered_plants = []
        for plant in plants:
            filtered_plant = {
                "common_name": plant.get("common_name", "N/A"),
                "scientific_name": plant.get("scientific_name", "N/A"),
                "image_url": plant.get("image_url", "N/A")
            }
            filtered_plants.append(filtered_plant)
        return filtered_plants
    else:
        print("Error:", response.text)
        return None


def save_data_to_json(data, file_name):
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    average_height = 6
    auth_token = os.getenv("AUTH_TOKEN")
    plant_data = get_plants_by_height(average_height, auth_token)
    if plant_data:
        folder_name = "data"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        file_name = (
            f"{folder_name}/filterByHeight_"
            f"{date.today().strftime('%Y-%m-%d')}.json"
        )
        save_data_to_json(plant_data, file_name)
        print(f"Data has been saved to {file_name}.")
    else:
        print("Failed to fetch plant data.")
