import requests
from requests import Response

session = requests.Session()
game_versions = session.get('https://ddragon.leagueoflegends.com/api/versions.json').json()
game_version = game_versions[0]  # Get latest game version


def get_file(filepath: str) -> Response:
    ddragon_url = f"https://ddragon.leagueoflegends.com/cdn/{game_version}/data/pt_BR/{filepath}"
    return session.get(ddragon_url)
