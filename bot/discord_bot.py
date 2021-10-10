import io
import discord
import os
import sys
import logging
import asyncio
from model.model import DialogueModel

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

        # Initialize a bot
        self.bot = None

    def get_token(self) -> str:
        return self.token

    def set_bot(self, bot: DialogueModel) -> None:
        # TODO: type checking for the bot
        self.bot = bot


    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))
        self.logger.info("CONNECTED.")

    async def on_message(self, message):
        if message.author == self.user:
            def check(reaction, user):
                if str(reaction.emoji) == '👍':
                    return user != message.author and str(reaction.emoji) == '👍'
                elif str(reaction.emoji) == '👎':
                    return user != message.author and str(reaction.emoji) == '👎'
            try:
                reaction, user = await self.wait_for('reaction_add', timeout=None, check=check)
            except asyncio.TimeoutError:
                self.logger.info("Reaction timeout.")
            else:
                # TODO: Write current message and response in a log for model analysis
                if str(reaction.emoji) == '👍':
                    await message.channel.send("Got a 👍")
                elif str(reaction.emoji) == '👎':
                    await message.channel.send("Got a 👎")
                

        if self.user.mentioned_in(message):
            print('Message from {0.author}: {0.content}'.format(message))
            #TODO: Read message
            #TODO: Strip user tags
            self.logger.info("Passing: " + "{0.content}".format(message))
            # Passes message input to bot and awaits the response
            response = self.bot.chat("{0.content}".format(message))
            self.logger.info("Received response: " + response)
            await message.channel.send(response)