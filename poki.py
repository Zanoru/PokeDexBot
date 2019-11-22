import requests
import json

def get_pokemon_data(name):
    req = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}/')
    if req.status_code != 200:
        return 'Error'
    
    req_data = req.json()
    
    pokemon_data = {
        'id': req_data['id'],
        'name': req_data['name'],
        'pokemonType': req_data['types'][0]['type']['name'],
        'height': req_data['height'],
        'weight': req_data['weight'],
        'sprites': req_data['sprites']['front_default']
    }
    
    return pokemon_data
