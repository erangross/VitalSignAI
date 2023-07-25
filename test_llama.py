import os
import transformers
import torch
from transformers import AutoTokenizer

api_key = os.environ.get("HF_API_KEY")


model = "meta-llama/Llama-2-7b-chat-hf"

tokenizer = AutoTokenizer.from_pretrained(model, use_auth_token=api_key)

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    device="cpu",
    use_auth_token=api_key,
    
)

sequences = pipeline(
    'I liked "Breaking Bad" and "Band of Brothers". Do you have any recommendations of other shows I might like?\n',
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    max_length=50,
)

for seq in sequences:
    print(f"Result: {seq['generated_text']}")