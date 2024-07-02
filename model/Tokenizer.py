import torch

"""
    -> Util functions for tokenizing Text based on Models Tokenizer and Limits.
"""

def tokenize_text(texts, tokenizer, max_length):
    tokenized_texts = []
    for text in texts:
        tokens = tokenizer(text)['input_ids']
        for i in range(0, len(tokens), max_length):
            chunk = tokens[i:i + max_length]
            if len(chunk) < max_length:
                chunk += [tokenizer.pad_token_id] * (max_length - len(chunk))
            tokenized_texts.append(torch.tensor(chunk))
    return tokenized_texts