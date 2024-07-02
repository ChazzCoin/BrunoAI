import torch
import Loader

"""

    -> Change the prompt at the bottom and run the script to test the model.
    -> Change the path to the model 'model_dir' to test different models.

"""
model_dir = './gpt2-ft4'

def generate_text(model, tokenizer, input_text, max_length=1024, num_return_sequences=1):
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    attention_mask = (input_ids != tokenizer.pad_token_id).long()
    input_ids = input_ids.to(model.device)
    attention_mask = attention_mask.to(model.device)
    with torch.no_grad():
        output_sequences = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=max_length,
            num_return_sequences=num_return_sequences,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
    for idx, output_sequence in enumerate(output_sequences):
        generated_text = tokenizer.decode(output_sequence, skip_special_tokens=True)
        print(f"Generated Text {idx + 1}: {generated_text}")

def chat(message):
    tokenizer, model = Loader.load_model(model_dir)
    generate_text(model, tokenizer, message)

if __name__ == "__main__":
    chat("the Christianization of the Roman Empire suppressed")