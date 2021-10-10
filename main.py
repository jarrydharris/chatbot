from bot.discord_bot import DiscordBot
from transformers import AutoModelForCausalLM, AutoTokenizer
from model.model import DialogueModel

if __name__ == "__main__":

    # Set up model
    print("Setting up model")
    model_size = "medium"
    tokenizer = AutoTokenizer.from_pretrained(f"microsoft/DialoGPT-{model_size}")
    model = AutoModelForCausalLM.from_pretrained(f"microsoft/DialoGPT-{model_size}")
    bot = DialogueModel(model, tokenizer)
    print("Done.")
    
    # Start Discord Client
    print("Starting Discord Client")
    client = DiscordBot()
    client.set_bot(bot)
    client.run(client.get_token())


