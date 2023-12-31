import concurrent
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple, Dict, Union

import data_dragon_connection
from abstract_league import Summoner, LeagueEntry, SummonerMatchData
from riot_api_connection import api_get

champion_data_list = data_dragon_connection.get_file('champion.json').json()  # type: Dict
champion_data_list = champion_data_list['data']
champion_by_key = {champion_data_list[champ_id]['key']: champion_data_list[champ_id] for champ_id in champion_data_list}


def request_match(tup: Tuple[str, str]) -> SummonerMatchData:
    summ_id, m_id = tup
    match_unit_resp = api_get('americas', f'/lol/match/v5/matches/{m_id}?count=3')
    match_data = match_unit_resp.json()

    players = match_data['info']['participants']
    player_id_filter = filter(lambda player_data: player_data['summonerId'] == summ_id, players)
    target_player = next(player_id_filter)  # Get a single player with the same summonerId (should be unique)

    return SummonerMatchData(
        kills=target_player['kills'],
        deaths=target_player['deaths'],
        assists=target_player['assists'],
        win=target_player['win']
    )


class Stats:
    def __init__(self, summoner: Summoner):
        self.summoner = summoner
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_queues = executor.submit(self._get_queues)
            future_mastery = executor.submit(self._get_top_mastery)
            future_hist = executor.submit(self._get_match_hist)

            self.hist = future_hist.result()
            self.mastery = future_mastery.result()
            self.queues = future_queues.result()

        matches_count = len(self.hist)
        total_kills = total_deaths = total_assists = 0

        for data in self.hist:
            total_kills += data.kills
            total_deaths += data.deaths
            total_assists += data.assists

        self.avg_kills = total_kills / matches_count
        self.avg_deaths = total_deaths / matches_count
        self.avg_assists = total_assists / matches_count

    def _get_queues(self) -> Union[None, List[LeagueEntry]]:
        queues_data_resp = api_get('br1', f'/lol/league/v4/entries/by-summoner/{self.summoner.summoner_id}')
        if queues_data_resp.status_code != 200:
            return None
        queues_data = queues_data_resp.json()
        queues = []

        for queue_data in queues_data:
            queues.append(LeagueEntry(
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

        return queues

    def _get_match_hist(self) -> Union[None, List[SummonerMatchData]]:
        matches_resp = api_get('americas', f"/lol/match/v5/matches/by-puuid/{self.summoner.encrypted_puuid}/ids")
        if matches_resp.status_code != 200:
            return None
        match_ids = matches_resp.json()

        with ThreadPoolExecutor(max_workers=3) as executor:
            future = executor.map(request_match, [
                (self.summoner.summoner_id, m) for m in match_ids]
                                  )
            return list(future)

    def _get_top_mastery(self) -> Union[None, List[Tuple[str, int, int]]]:
        puuid = self.summoner.encrypted_puuid
        response = api_get('br1', f'/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top?count=3')
        if response.status_code != 200:
            return None

        response_data = response.json()

        mastery_list = []
        for mastery_item in response_data:
            # For some reason, Data Dragon has Keys saved as strings, but the API returns them as integers
            champion_key = str(mastery_item['championId'])
            mastery_level = mastery_item['championLevel']
            mastery_points = mastery_item['championPoints']

            champion_name = champion_by_key[champion_key]['name']

            mastery_list.append((champion_name, mastery_level, mastery_points))

        return mastery_list


def get_stats(summoner: Summoner) -> Stats:
    return Stats(summoner)
