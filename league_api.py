"""
Interface to pull data with the League of Legends API
"""

from datetime import datetime, timedelta

# Contains a list of pairs of Summoner objects, generated from the pulled data, and the time of cache
CACHE = {}  # type: dict[str, CachedSummonerWrapper]
CACHE_LIFETIME = 30  # Lifetime, in seconds, of cached items


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


class CachedSummonerWrapper:
    def __init__(self, summoner: Summoner, cache_expiration_time: datetime):
        self.summoner = summoner
        self.cache_expiration_time = cache_expiration_time

    def is_valid(self) -> bool:
        return self.cache_expiration_time < datetime.now()


def pull_summoner(summoner_name: str) -> Summoner:
    # This is the only point Cache is ever altered, therefore, it is the only time in which it needs to be sanitized
    update_cache()
    if summoner_name in CACHE:
        return CACHE[summoner_name].summoner
    else:
        summoner_data = None  # type: Summoner  # TODO: Implement with League API
        expiration_time = datetime.now() + timedelta(seconds=CACHE_LIFETIME)
        CACHE[summoner_name] = CachedSummonerWrapper(summoner_data, expiration_time)
        return summoner_data


def update_cache() -> None:
    global CACHE
    CACHE = {summ_name: cached_summ for summ_name, cached_summ in CACHE.items() if cached_summ.is_valid()}
