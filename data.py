import requests
import json

def find_pokemon(pokemon):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}/'
    req = requests.get(url)
    content = json.loads(req.content)

    return content


