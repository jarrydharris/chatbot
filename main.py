from bot.discord_bot import DiscordBot

if __name__ == "__main__":
    client = DiscordBot()
    client.run(client.get_token())
