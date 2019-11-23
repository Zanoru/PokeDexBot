import requests
import json

def get_pokemon_data(name):
    req = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}/')
    if req.status_code != 200:
        return 'Error'
    
    req_data = req.json()
    
    pokemon_data = {
        '_id': req_data['id'],
        'name': req_data['name'],
        'height': req_data['height'],
        'pokemonType': [el['type']['name'] for el in req_data['types']],
        'weight': req_data['weight'],
        'sprites': req_data['sprites']['front_default']
    }
    
    return pokemon_data

