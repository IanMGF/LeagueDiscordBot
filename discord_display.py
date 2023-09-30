from time import strftime, localtime

from discord import Embed
from discord.ext.commands import Context

import league_api
from league_api import Summoner

"""
Interface to convert data from League API to Discord objects, that can be displayed as an Embedded
"""


class SummonerDiscordDisplay:
    def __init__(self, summoner: Summoner):
        self.summoner = summoner

    async def display(self, ctx: Context):
        # revision_date is given in milliseconds, localtime takes seconds
        last_modification = strftime('%H:%M do dia %d/%m/%Y', localtime(self.summoner.revision_date / 1000))
        last_load_time = league_api.get_cache_origin(self.summoner.name).strftime('%H:%M:%S')

        queues_info = self.summoner.get_stats().get_queues()

        embed = Embed(title=self.summoner.name,
                      description=f"Informações sobre o usuário {self.summoner.name} [Servidor BR1]",
                      color=0xd4d4d4)

        embed.set_thumbnail(
            url=f"https://ddragon.leagueoflegends.com/cdn/13.19.1/img/profileicon/{self.summoner.profile_icon_id}.png"
        )

        embed.add_field(name="Nome de usuário", value=self.summoner.name, inline=True)
        embed.add_field(name="Nível", value=f"{self.summoner.summoner_level}", inline=True)

        # Queues
        for queue in queues_info:
            embed.add_field(name=f'Fila: {queue.queue_type}',
                            value=f'Vitórias: {queue.wins}\n' 
                                  f'Derrotas: {queue.losses}\n'
                                  f'Rank: {queue.tier} - {queue.division}', inline=False)

        embed.add_field(name="Última modificação no perfil", value=f"{last_modification}", inline=False)
        embed.set_footer(
            text=f"[Essas informações foram adquiridas pela API pública de League of Legends ({last_load_time})]"
        )

        await ctx.send(embed=embed)
