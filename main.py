from discord.ext.commands import Bot, Context
from discord import Intents

import league_api
import tokens
from discord_display import SummonerDiscordDisplay

intents = Intents.default()
intents.message_content = True

bot = Bot('!', intents=intents)


@bot.command('user')
async def show_user_data(ctx: Context, username: str):
    summ = league_api.pull_summoner(username)

    if summ is None:
        await ctx.send(f"Houve um erro ao tentar acessar os dados de {username} :(")

    else:
        discord_summ = SummonerDiscordDisplay(summ)
        await discord_summ.display(ctx)

tokens.init_tokens()

bot.run(tokens.DISCORD_TOKEN)
