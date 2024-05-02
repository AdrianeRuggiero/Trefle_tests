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

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  

        if response.status_code == 200:
            plants_data = response.json()["data"]  # Obter os dados das plantas
            plants_info = []  # Inicializar a lista para armazenar informações das plantas

            for plant in plants_data:
                scientific_name = plant.get("scientific_name", "N/A")  # Nome científico da planta
                image_url = plant.get("image_url", "N/A")  # URL da imagem da planta
                plants_info.append({"scientific_name": scientific_name, "image_url": image_url})

            return plants_info
        else:
            print("Error:", response.text)
            return None

    except requests.exceptions.RequestException as e:
        print("Error fetching plant data:", e)
        return None

# Verifica se o arquivo está sendo executado diretamente
if __name__ == "__main__":
    # Exemplo de uso apenas para o arquivo original
    common_name = "Lavender"

    plant_data = get_plants_by_common_name(common_name, os.getenv("AUTH_TOKEN"))
    if plant_data:
        for plant in plant_data:
            print("Scientific Name:", plant["scientific_name"])
            print("Image URL:", plant["image_url"])
            print()
    else:
        print("Maluco!")
