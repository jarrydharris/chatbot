import discord
import os
import sys

class DiscordBot(discord.Client):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.token = os.getenv('DISCORD_TOKEN')
        if self.token is None:
            print("ERROR:")
            print("\tPlease set DISCORD_TOKEN environment variable.")
            print("\tExiting...")
            sys.exit()


    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))

    async def on_message(self, message):
        if message.author == self.user:
            return
        


p = DiscordBot()