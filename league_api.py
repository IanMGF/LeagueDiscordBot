"""
Interface to pull data with the League of Legends API
"""

# This is a bad fix to avoid a cyclic dependency between league_api and league_stats.
# Ideally, this ought to be split into 3 files:
# 1 - Classes, for abstractions of League API,
# 2 - A connection with the League API
# 3 - A file to calculate statistics about the player

from datetime import datetime, timedelta
from typing import Union

import requests

import tokens
from tokens import RIOT_API_BASE
from league_stats import Stats

# Contains a list of pairs of Summoner objects, generated from the pulled data, and the time of cache
CACHE = {}  # type: dict[str, CachedSummonerWrapper]
CACHE_LIFETIME = 60  # Lifetime, in seconds, of cached items


class Summoner:
    def __init__(self, name, account_id, profile_icon_id, revision_date,
                 summoner_id, encrypted_puuid, summoner_level):
        self.name = name
        self.account_id = account_id
        self.profile_icon_id = profile_icon_id
        self.revision_date = revision_date
        self.summoner_id = summoner_id
        self.encrypted_puuid = encrypted_puuid
        self.summoner_level = summoner_level
        self.__stats__ = None

    def get_stats(self) -> Stats:
        if self.__stats__ is None:
            self.__stats__ = Stats(self.summoner_id)
        return self.__stats__


class CachedSummonerWrapper:
    def __init__(self, summoner: Summoner, cache_expiration_time: datetime):
        self.summoner = summoner
        self.cache_expiration_time = cache_expiration_time

    def is_valid(self) -> bool:
        return self.cache_expiration_time > datetime.now()


def pull_summoner(summoner_name: str) -> Union[Summoner, None]:
    # This is the only point Cache is ever altered, therefore, it is the only time in which it needs to be sanitized
    update_cache()

    if summoner_name in CACHE.keys():
        return CACHE[summoner_name].summoner
    else:
        # summoner_data = None  # type: Summoner
        resp = requests.get(f"{RIOT_API_BASE}/lol/summoner/v4/summoners/by-name/{summoner_name}",
                            headers={'X-Riot-Token': tokens.RIOT_TOKEN})

        if resp.status_code != 200:
            with open(f"dumps/response_dump_{summoner_name}_{datetime.now().strftime('%H%M%S')}", "w") as response_dump:
                response_dump.write(resp.text)
            return None

        summoner_data = resp.json()

        summoner = Summoner(
            name=summoner_data['name'],
            account_id=summoner_data['accountId'],
            profile_icon_id=summoner_data['profileIconId'],
            revision_date=summoner_data['revisionDate'],
            summoner_id=summoner_data['id'],
            encrypted_puuid=summoner_data['puuid'],
            summoner_level=summoner_data['summonerLevel']
        )

        expiration_time = datetime.now() + timedelta(seconds=CACHE_LIFETIME)
        CACHE[summoner_name] = CachedSummonerWrapper(summoner, expiration_time)
        return summoner


def get_cache_origin(summoner_name: str) -> Union[None, datetime]:
    if summoner_name not in CACHE:
        return datetime.now()

    return CACHE[summoner_name].cache_expiration_time


def update_cache() -> None:
    global CACHE
    CACHE = {summ_name: cached_summ for summ_name, cached_summ in CACHE.items() if cached_summ.is_valid()}
