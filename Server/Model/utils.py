import requests, json
from langchain.tools import tool

@tool
def get_stats(name: str) -> str:
    """retrieves the stats from the pokemon API for a given pokemon name"""
    API_URL = f'https://pokeapi.co/api/v2/pokemon/{name.lower().strip()}'
    result = requests.get(API_URL)
    data = json.loads(result.content)

    pk_data = {
        'id': data['id'],
        'name': data['name'],
        'types': len(data['types'])
    }

    # add the types
    pk_data['type1'] = data['types'][0]['type']['name'],
    pk_data['type2'] = data['types'][1]['type']['name'] if len(data['types']) > 1 else None

    # add the move, ability and form counts
    pk_data['move_count'] = len(data['moves'])
    pk_data['ability_count'] = len(data['abilities'])
    pk_data['form_count'] = len(data['forms'])

    # add the base stats
    stats = {}
    for stat in data['stats']:
        stat_name = stat['stat']['name']
        stats[stat_name] = stat['base_stat']
        stats[stat_name + '_effort'] = stat['effort']
    pk_data['stats'] = stats

    # add the currently available abbilities
    ab_set = []
    for ability in data['abilities']:
        ab_set.append({
            'name': ability['ability']['name'],
            'is_hidden': ability['is_hidden'],
        })
    pk_data['abilities'] = ab_set
    result_str = (
        f'name: {pk_data['name']} | '
        f'pokedex id: {pk_data['id']} | '
        f'types: {pk_data['types']} | '
        f'type 1: {pk_data['type1']} | '
        f'type 2: {pk_data['type2']} | '
        f'move count: {pk_data['move_count']} | '
        f'ability count: {pk_data['ability_count']} | '
        f'form count: {pk_data['form_count']} | '
        f'stats: {pk_data['stats']} |'
        f'abilities: {pk_data['abilities']}'
    )

    print("Current PK Data: ", result_str)
    return result_str