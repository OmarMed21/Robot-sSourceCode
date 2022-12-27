import string

from transformers import GPT2LMHeadModel, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)


text = "what's Programming?"
encoded_input = tokenizer.encode(text, return_tensors="pt")

generator = model.generate(
    encoded_input,
    max_length=100,
    num_beams=5,
    no_repeat_ngram_size=2,
    early_stopping=True,
)

output = (
    tokenizer.decode(generator[0], skip_special_tokens=True)
    .translate(str.maketrans("", "", string.punctuation))
    .replace("\n", " ")[len(text) :]
)
print(output)
