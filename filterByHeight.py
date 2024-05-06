import requests
import json
from datetime import date
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()


def get_plants_by_height(average_height, auth_token):
    """
    Fetches plant data based on the specified average height.

    Parameters:
        average_height (int): The average height of plants to filter.
        auth_token (str): The authentication token for accessing the API.

    Returns:
        dict: A dictionary containing filtered plant data,
        along with the date and average height.
              Returns None if there's an error.
    """
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

        # Add the date and average height to the filtered data
        filtered_data = {
            "date": date.today().strftime('%Y-%m-%d'),
            "average_height_cm": average_height,
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


def create_file_name(folder_name="data", file_prefix="filterByHeight_"):
    """
    Creates a file name based on the current date.

    Parameters:
        folder_name (str): The name of the folder to save the file in.
                           Defaults to "data".
        file_prefix (str): The prefix to be added to the file name.
                           Defaults to "filterByHeight_".

    Returns:
        str: The generated file name.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return os.path.join(
        folder_name,
        f"{file_prefix}{date.today().strftime('%Y-%m-%d')}.json"
    )


if __name__ == "__main__":
    average_height = 5
    auth_token = os.getenv("AUTH_TOKEN")
    plant_data = get_plants_by_height(average_height, auth_token)
    if plant_data:
        file_name = create_file_name()
        save_data_to_json(plant_data, file_name)
        print(f"Data has been saved to {file_name}.")
    else:
        print("Failed to fetch plant data.")
