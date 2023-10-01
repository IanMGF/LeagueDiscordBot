from typing import Dict

import requests
from requests import Session

import tokens


HEADERS = {'X-Riot-Token': tokens.RIOT_TOKEN}
ROUTE_VALUES = ('br1', 'americas')


def init_session(route_value) -> Session:
    session = requests.Session()
    session.headers['X-Riot-Token'] = tokens.RIOT_TOKEN
    session.get(f"https://{route_value}.api.riotgames.com/")
    return session


SESSIONS = {route: init_session(route) for route in ROUTE_VALUES}  # type: Dict[str, Session]


def api_get(route_value, endpoint):
    url = f"https://{route_value}.api.riotgames.com{endpoint}"
    session = SESSIONS[route_value]
    response = session.get(url)
    return response
