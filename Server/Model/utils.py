import requests
from langchain.tools import tool

@tool
def get_stats(name: str) -> str:
    """retrieves the stats from the pokemon API for a given pokemon name"""
    API_URL = f'https://pokeapi.co/api/v2/pokemon/{name.lower().strip()}'
    result = requests.get(API_URL)
    return result.json()