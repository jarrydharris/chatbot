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

        self.bot_input_ids = None
        self.chat_history_ids = None

    def chat(self, message: str) -> str:
        new_user_input_ids = self.tokenizer.encode(message + self.tokenizer.eos_token, 
            return_tensors='pt')
        self.bot_input_ids = torch.cat([self.chat_history_ids, new_user_input_ids], dim=-1) if self.bot_input_ids is not None else new_user_input_ids
        self.chat_history_ids = self.model.generate(self.bot_input_ids, max_length=10000, pad_token_id=self.tokenizer.eos_token_id, temperature=0.6, repetition_penalty=1.3)

        # print("Message: ", message)
        # print("new_user_input_ids: ", str(new_user_input_ids))
        # print("bot_input_ids: ", str(self.bot_input_ids))
        # print("chat_history_ids: ", str(self.chat_history_ids))


        return "{}".format(self.tokenizer.decode(self.chat_history_ids[:, self.bot_input_ids.shape[-1]:][0], skip_special_tokens=True))


