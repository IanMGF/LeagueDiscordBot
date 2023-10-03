from typing import Dict

import requests
from requests import Session, Response

import tokens


HEADERS = {'X-Riot-Token': tokens.RIOT_TOKEN}
ROUTE_VALUES = ('br1', 'americas')


def init_session(route_value: str) -> Session:
    session = requests.Session()
    session.headers['X-Riot-Token'] = tokens.RIOT_TOKEN
    session.get(f"https://{route_value}.api.riotgames.com/")
    return session


SESSIONS = {route: init_session(route) for route in ROUTE_VALUES}  # type: Dict[str, Session]


def api_get(route_value: str, endpoint: str) -> Response:
    url = f"https://{route_value}.api.riotgames.com{endpoint}"
    session = SESSIONS[route_value]
    response = session.get(url)
    return response
