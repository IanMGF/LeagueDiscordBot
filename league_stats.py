from typing import List

import requests

from tokens import RIOT_API_BASE
import tokens


class LeagueEntry:
    def __init__(self, queue_type, tier, division, league_points, wins, losses, hot_streak, veteran,
                 fresh_blood, inactive):
        self.queue_type = queue_type
        self.tier = tier
        self.division = division
        self.league_points = league_points
        self.wins = wins
        self.losses = losses
        self.hot_streak = hot_streak
        self.veteran = veteran
        self.fresh_blood = fresh_blood
        self.inactive = inactive


class Stats:
    def __init__(self, summoner_id: str):
        self.summoner_id = summoner_id
        self.__queues__ = None

    def get_queues(self) -> List[LeagueEntry]:
        if self.__queues__ is None:
            queues_data_resp = requests.get(f'{RIOT_API_BASE}/lol/league/v4/entries/by-summoner/{self.summoner_id}',
                                            headers={'X-Riot-Token': tokens.RIOT_TOKEN})
            queues_data = queues_data_resp.json()
            self.__queues__ = []

            for queue_data in queues_data:
                self.__queues__.append(LeagueEntry(
                    queue_type=queue_data['queueType'],
                    tier=queue_data['tier'],
                    division=queue_data['rank'],
                    league_points=queue_data['leaguePoints'],
                    wins=queue_data['wins'],
                    losses=queue_data['losses'],
                    hot_streak=queue_data['hotStreak'],
                    veteran=queue_data['veteran'],
                    fresh_blood=queue_data['freshBlood'],
                    inactive=queue_data['inactive']
                ))

        return self.__queues__
