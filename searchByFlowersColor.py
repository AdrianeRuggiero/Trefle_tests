import requests
import json
from datetime import date
from dotenv import load_dotenv
import os
from urllib.parse import urlencode

# Load environment variables from the .env file
load_dotenv()


def get_plants_by_flower_color(flower_color, auth_token):
    """
    Fetches plant data based on the specified flower color.

    Parameters:
        flower_color (str): The color of flowers to filter.
        auth_token (str): The authentication token for accessing the API.

    Returns:
        dict: A dictionary containing filtered plant data,
        along with the date and flower color.
              Returns None if there's an error.
    """
    url = "https://trefle.io/api/v1/species"
    params = {
        "token": auth_token,
        "filter[flower_color]": flower_color
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

        # Add the date and flower color to the filtered data
        filtered_data = {
            "date": date.today().strftime('%Y-%m-%d'),
            "flower_color": flower_color,
            "plants": filtered_plants
        }

        return filtered_data
    else:
        print("Error:", response.text)
        return None


def save_data_to_json(data, file_name):
    """
    Saves data to a JSON file.

    Parameters:
        data (dict): The data to be saved.
        file_name (str): The name of the file to save the data to.
    """
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)


def generate_google_search_link(plant):
    """
    Generates a Google search link with the scientific name of the plant.

    Parameters:
        plant (dict): A dictionary containing information about a plant.

    Returns:
        str: The Google search link.
    """
    base_url = "https://www.google.com/search?"
    query_params = {"q": plant["scientific_name"]}
    return base_url + urlencode(query_params)


def create_file_name(folder_name="data", file_prefix="filterByFlowerColor_"):
    """
    Creates a file name based on the current date.

    Parameters:
        folder_name (str): The name of the folder to save the file in.
                           Defaults to "data".
        file_prefix (str): The prefix to be added to the file name.
                           Defaults to "filterByFlowerColor_".

    Returns:
        str: The generated file name.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return os.path.join(
        folder_name,
        f"{file_prefix}{date.today().strftime('%Y-%m-%d')}.json"
    )


def fetch_and_save_plant_data(flower_color, auth_token):
    plant_data = get_plants_by_flower_color(flower_color, auth_token)
    if plant_data:
        for plant in plant_data["plants"]:
            plant["google_search_link"] = generate_google_search_link(plant)

        file_name = create_file_name()
        save_data_to_json(plant_data, file_name)
        print(f"Data has been saved to {file_name}.")
    else:
        print("Failed to fetch plant data.")


if __name__ == "__main__":
    flower_color = "red"
    auth_token = os.getenv("AUTH_TOKEN")
    fetch_and_save_plant_data(flower_color, auth_token)
