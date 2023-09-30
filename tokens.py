"""
This method of storing API keys has 2 main issues:
- It is sensitive to alterations on the file (hopefully blocked by OS configuration)
- It may be stolen by anyone with access to the file

Yet, given the simplicity of the project, it is enough.

The TOKENS.txt file is supposed to have only 2 lines of text:
Line 1: Discord Bot Token
Line 2: Riot API Token
"""

import discord

DISCORD_TOKEN = ""
RIOT_TOKEN = ""


def init_tokens():
    with open('TOKENS.txt', 'r') as token_file:
        global DISCORD_TOKEN
        global RIOT_TOKEN

        tokens = token_file.readlines()
        DISCORD_TOKEN = tokens[0]
        RIOT_TOKEN = tokens[1]
