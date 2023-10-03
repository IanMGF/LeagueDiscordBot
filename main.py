from discord.ext.commands import Bot, Context
from discord import Intents

import tokens
import league_api
from league_api import CachedSummonerWrapper
from discord_display import SummonerDiscordDisplay

intents = Intents.default()
intents.message_content = True

bot = Bot('!', intents=intents)


@bot.command('user')
async def show_user_data(ctx: Context, username: str) -> None:
    temp_msg = await ctx.send("Adquirindo dados do perfil... (Isso pode levar alguns segundos)")
    summ = league_api.pull_summoner(username)  # type: CachedSummonerWrapper

    if summ is None:
        await temp_msg.edit(content=f"Houve um erro ao tentar acessar os dados de {username} :(")

    else:
        discord_summ = SummonerDiscordDisplay(summ)
        dc_view_embed = discord_summ.gen_embed()
        await temp_msg.edit(content='', embed=dc_view_embed)

bot.run(tokens.DISCORD_TOKEN)
