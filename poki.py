import requests
import json
import random

data = {
    "normal": "🏷️",
    "fire": "🔥",
    "grass": "🌿",
    "electric": "⚡",
    "poison": "🤢",
    "water": "🌊",
    "bug": "🐛",
    "fairy": "🧚",
    "ground": "🌱",
    "fighting": "👊",
    "rock": "🌚",
    "steel": "⚙️",
    "ice": "❄",
    "ghost": "👻",
    "flying": "🐦",
    "dragon": "🐉",
    "dark": "⚫",
    "psychic": "🌀"
}

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
    
    
def get_random_pokemon():
    random_id = random.randint(1, 809)
    
    req = requests.get(f'https://pokeapi.co/api/v2/pokemon/{random_id}/')
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
    

def get_pokemontype_emoji(pokemonType):
    return data[pokemonType]
