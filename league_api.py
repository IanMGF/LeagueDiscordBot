"""
Interface to pull data with the League of Legends API
"""


from datetime import datetime, timedelta
from typing import Union, Dict

from abstract_league import Summoner
from riot_api_connection import api_get
from league_stats import Stats

# Contains a list of pairs of Summoner objects, generated from the pulled data, and the time of cache
CACHE = {}  # type: Dict[str, CachedSummonerWrapper]
CACHE_LIFETIME = 120  # Lifetime, in seconds, of cached items


class CachedSummonerWrapper:
    def __init__(self, summoner: Summoner, cache_expiration_time: datetime):
        self.summoner = summoner
        self.stats = Stats(summoner)
        self.cache_expiration_time = cache_expiration_time

    def is_valid(self) -> bool:
        return self.cache_expiration_time > datetime.now()


def pull_summoner(summoner_name: str) -> Union[CachedSummonerWrapper, None]:
    # This is the only point Cache is ever altered, therefore, it is the only time in which it needs to be sanitized
    update_cache()

    if summoner_name in CACHE:
        return CACHE[summoner_name]

    else:
        resp = api_get('br1', f"/lol/summoner/v4/summoners/by-name/{summoner_name}")

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
            summoner_level=summoner_data['summonerLevel'],
        )

        expiration_time = datetime.now() + timedelta(seconds=CACHE_LIFETIME)
        cached_summoner = CachedSummonerWrapper(summoner, expiration_time)
        CACHE[summoner_name] = cached_summoner
        return cached_summoner


def update_cache() -> None:
    global CACHE
    CACHE = {summ_name: cached_summ for summ_name, cached_summ in CACHE.items() if cached_summ.is_valid()}
