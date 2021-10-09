import discord
import os
import sys
import logging

LOG_PATH = "./logs/discord.log"

class DiscordBot(discord.Client):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Logger setup
        self.logger = logging.getLogger('discord')
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.FileHandler(filename=LOG_PATH, encoding='utf-8', mode='a')
        self.handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(self.handler)
        self.logger.info("STARTING SESSION.")

        # Get discord api token from environment variable
        self.token = os.getenv('DISCORD_TOKEN')
        if self.token is None:
            print("ERROR:")
            print("\tPlease set DISCORD_TOKEN environment variable.")
            self.logger.debug("ERROR: token was None.")
            print("\tExiting...")
            sys.exit()

    def get_token(self):
        return self.token

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))
        self.logger.info("CONNECTED.")

    async def on_message(self, message):
        if message.author == self.user:
            return
        