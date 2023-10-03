from time import strftime, localtime

from discord import Embed, Message

from league_api import CachedSummonerWrapper

"""
Interface to convert data from League API to Discord objects, that can be displayed as an Embedded
"""


class SummonerDiscordDisplay:
    def __init__(self, cached_summoner: CachedSummonerWrapper):
        self.cached_wrapper = cached_summoner
        self.summoner = cached_summoner.summoner

    def gen_embed(self) -> Embed:
        # revision_date is given in milliseconds, localtime takes seconds
        last_profile_mod = strftime('%H:%M do dia %d/%m/%Y', localtime(self.summoner.revision_date / 1000))
        last_load_time = self.cached_wrapper.cache_expiration_time.strftime('%H:%M:%S')

        summ_stats = self.cached_wrapper.stats
        queues_info = summ_stats.queues

        embed = Embed(title=self.summoner.name,
                      description=f"Informações sobre o(a) usuário(a) {self.summoner.name} [Servidor BR1]",
                      color=0xd4d4d4)

        # Icon
        embed.set_thumbnail(
            url=f"https://ddragon.leagueoflegends.com/cdn/13.19.1/img/profileicon/{self.summoner.profile_icon_id}.png"
        )

        # Level
        embed.add_field(name="Nível", value=f"{self.summoner.summoner_level}", inline=True)

        # Average KDA
        avg_kills = summ_stats.avg_kills
        avg_deaths = summ_stats.avg_deaths
        avg_assists = summ_stats.avg_assists
        embed.add_field(name='K/D/A Médio',
                        value=f'{avg_kills} / {avg_deaths} / {avg_assists}\n(Últimas {len(summ_stats.hist)} partidas)',
                        inline=True)

        # Most mastery points
        embed.add_field(name="Maiores maestrias",
                        value='\n'.join([f"{mast[0]} - M{mast[1]} ({mast[2]} pts)" for mast in summ_stats.mastery]),
                        inline=False)

        # Queues
        for queue in queues_info:
            embed.add_field(name=f'Ranqueada - Fila {queue.queue_name}',
                            value=f'Rank: {queue.tier} {queue.division}\n'
                                  f'Vitórias: {queue.wins}\n'
                                  f'Derrotas: {queue.losses}\n',
                            inline=False)

        embed.add_field(name="Última modificação no perfil", value=f"{last_profile_mod}", inline=False)

        embed.set_footer(
            text=f"[Essas informações foram adquiridas pela API pública de League of Legends ({last_load_time})]"
        )

        return embed
