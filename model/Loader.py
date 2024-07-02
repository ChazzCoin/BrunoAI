import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel

"""
    -> Util functions for loading and saving models
"""

def load_model(model_dir, model_name='gpt2'):
    if os.path.exists(model_dir):
        tokenizer = GPT2Tokenizer.from_pretrained(model_dir)
        model = GPT2LMHeadModel.from_pretrained(model_dir)
        print(f"Loaded saved model from {model_dir}")
    else:
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        tokenizer.pad_token = tokenizer.eos_token
        model = GPT2LMHeadModel.from_pretrained(model_name)
        model.resize_token_embeddings(len(tokenizer))
        print("No saved model found. Created a new model.")
    return tokenizer, model

def save_model(model, tokenizer, output_dir):
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)