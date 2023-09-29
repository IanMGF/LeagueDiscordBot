from time import strftime, localtime

from discord import Embed
from discord.ext.commands import Context

from league_api import Summoner

"""
Interface to convert data from League API to Discord objects, that can be displayed as an Embedded
"""


class SummonerDiscordDisplay:
    def __init__(self, summoner: Summoner):
        self.summoner = summoner

    async def display(self, ctx: Context):
        last_modification = strftime('%H:%M do dia %d/%m/%Y', localtime(self.summoner.revision_date))
        last_load_time = strftime('%H:%M:%s', localtime(None))  # TODO: Load datetime from cached info

        embed = Embed(title=f"Informações de {self.summoner.name}",
                      description=f"Informações sobre o usuário {self.summoner.name} [Servidor BR]",
                      color=0xd4d4d4)

        embed.set_thumbnail(
            url=f"https://ddragon.leagueoflegends.com/cdn/13.19.1/img/profileicon/{self.summoner.profile_icon_id}.png"
        )

        embed.add_field(name="Nome de usuário", value=self.summoner.name, inline=True)
        embed.add_field(name="Nível", value=f"{self.summoner.summoner_level}", inline=True)
        embed.add_field(name="Última modificação", value=f"{last_modification}", inline=False)
        embed.set_footer(
            text=f"[Essas informações foram adquiridas pela API pública de League of Legends ({last_load_time})]"
        )

        await ctx.send(embed=embed)
