"""
This method of storing the API key has some issues:
- It is sensitive to alterations on the file (hopefully blocked by OS configuration)
- It may be stolen by anyone with access to the file
"""

import discord


def connect_token(client: discord.Client):
    with open('TOKEN.txt', 'r') as token_file:
        token = token_file.read()
        client.run(token)
