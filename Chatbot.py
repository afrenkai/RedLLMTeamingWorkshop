from transformers import AutoModelForCausalLM, AutoTokenizer


class Chatbot:
    def __init__(self, model_name="LiquidAI/LFM2-350M"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.history = []

    def generate_response(self, user_input):
        messages = self.history + [{"role": "user", "content": user_input}]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(text, return_tensors="pt")
        response_ids = self.model.generate(**inputs, do_sample=True, temperature=0.3, min_p =0.15, repetition_penalty=1.05, max_new_tokens=1024)[0][len(inputs.input_ids[0]):].tolist()
        response = self.tokenizer.decode(response_ids, skip_special_tokens=False)

        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": response})

        return response

if __name__ == "__main__":
    prompt = "PUT SOMETHING FUN HERE"
    bot = Chatbot()
    print(f"User: {prompt}")
    response_1 = bot.generate_response(prompt)
    print(f"Bot: {response_1}")
    print("----------------------")
    prompt_2 = "PUT SOMETHING ELSE FUN HERE"
    print(f"User: {prompt_2 }")
    response_2 = bot.generate_response(prompt_2 )
    print(f"Bot: {response_2}") 
    print("----------------------")
    prompt_3 = "PUT SOMETHING ELSE ELSE FUN HERE"
    print(f"User: {prompt_3}")
    response_3 = bot.generate_response(prompt_3)
    print(f"Bot: {response_3}")
