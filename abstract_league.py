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


class LeagueEntry:
    QUEUE_NAMES = {
        'RANKED_SOLO_5x5': 'Solo/Duo',
        'RANKED_FLEX_SR': 'Flex',
    }

    def __init__(self, queue_type, tier, division, league_points, wins, losses, hot_streak, veteran,
                 fresh_blood, inactive):
        self.queue_type = queue_type
        self.queue_name = LeagueEntry.QUEUE_NAMES.get(queue_type, queue_type)
        self.tier = tier
        self.division = division
        self.league_points = league_points
        self.wins = wins
        self.losses = losses
        self.hot_streak = hot_streak
        self.veteran = veteran
        self.fresh_blood = fresh_blood
        self.inactive = inactive


class SummonerMatchData:
    # A huge chunk of data is intentionally left out, for it is incredibly unnecessary
    def __init__(self, kills, deaths, assists, win):
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.win = win
