import torch

class DialogueModel:
    def __init__(self, model, tokenizer) -> None:
        """
        This class is set up to act as the link between model building and the chatbot app. 
        Any DialogueModel will have a model, tokenizer and a chat function that takes in a
        message and returns a response based on the conversational model. 
        """
        self.model = model
        self.tokenizer = tokenizer
        # TODO: Handle large chat histories

        # TODO: Blank tensors
        self.bot_input_ids = torch.Tensor()
        self.chat_history_ids = torch.Tensor()

    def chat(self, message: str) -> str:
        new_user_input_ids = self.tokenizer.encode(message + self.tokenizer.eos_token, 
            return_tensors='pt')
        self.bot_input_ids = torch.cat([self.chat_history_ids, new_user_input_ids], dim=-1) if len(self.bot_input_ids) > 0 else new_user_input_ids
        chat_history_ids = self.model.generate(self.bot_input_ids, max_length=10000, pad_token_id=self.tokenizer.eos_token_id)

        return "DialoGPT: {}".format(self.tokenizer.decode(chat_history_ids[:, self.bot_input_ids.shape[-1]:][0], skip_special_tokens=True))


