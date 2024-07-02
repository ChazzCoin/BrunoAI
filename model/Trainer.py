import os

import Loader, Tokenizer
from transformers import Trainer, TrainingArguments
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split
from F import OS

class TextDataset(Dataset):
    def __init__(self, tokenized_texts, tokenizer):
        self.tokenized_texts = tokenized_texts
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.tokenized_texts)

    def __getitem__(self, idx):
        input_ids = self.tokenized_texts[idx]
        return {
            'input_ids': input_ids,
            'attention_mask': (input_ids != self.tokenizer.pad_token_id).long(),
            'labels': input_ids
        }

def main():
    # TODO: move this to a config based file/setup
    file_path = f"{os.getcwd()}/../dataset/pdf_training_data-gpt4-6.json"  # Path to your JSON file containing the document texts
    model_name = 'gpt2'
    output_dir = './gpt2-ft4'
    max_length = 512
    batch_size = 2
    num_epochs = 1

    # Load the Model and its Tokenizer.
    tokenizer, model = Loader.load_model(output_dir, model_name)

    # -> Load and Tokenize the Dataset.
    raw_data = OS.load_dict_from_file(file_path)
    texts = raw_data[0]['training']
    tokenized_texts = Tokenizer.tokenize_text(texts, tokenizer, max_length)

    # Split Dataset into Training/Validation Sets.
    train_texts, val_texts = train_test_split(tokenized_texts, test_size=0.1)
    train_dataset = TextDataset(train_texts, tokenizer)
    val_dataset = TextDataset(val_texts, tokenizer)

    # Create Training Arguments Instance
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=num_epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        warmup_steps=10,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
        save_steps=10,
        save_total_limit=2,
    )
    # Create Trainer Instance
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset
    )
    # Run Trainer
    trainer.train()
    # Save the model once Training has complete.
    Loader.save_model(model, tokenizer, output_dir)

if __name__ == "__main__":
    main()