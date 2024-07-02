import os
import torch

from transformers import (
    GPT2Tokenizer, GPT2LMHeadModel, BertTokenizer, BertForSequenceClassification,
    RobertaTokenizer, RobertaForSequenceClassification, DistilBertTokenizer, DistilBertForSequenceClassification,
    AlbertTokenizer, AlbertForSequenceClassification, T5Tokenizer, T5ForConditionalGeneration,
    XLNetTokenizer, XLNetLMHeadModel, OpenAIGPTTokenizer, OpenAIGPTLMHeadModel, BartTokenizer,
    BartForConditionalGeneration
)


class ModelProvider:
    MODEL_CLASSES = {
        'gpt2': (GPT2Tokenizer, GPT2LMHeadModel),
        'bert': (BertTokenizer, BertForSequenceClassification),
        'roberta': (RobertaTokenizer, RobertaForSequenceClassification),
        'distilbert': (DistilBertTokenizer, DistilBertForSequenceClassification),
        'albert': (AlbertTokenizer, AlbertForSequenceClassification),
        't5': (T5Tokenizer, T5ForConditionalGeneration),
        'xlnet': (XLNetTokenizer, XLNetLMHeadModel),
        'openai-gpt': (OpenAIGPTTokenizer, OpenAIGPTLMHeadModel),
        'bart': (BartTokenizer, BartForConditionalGeneration),
    }

    def __init__(self, model_name='gpt2'):
        self.model_name = model_name

    def load_model(self, model_dir):
        tokenizer_class, model_class = self.MODEL_CLASSES.get(self.model_name, (GPT2Tokenizer, GPT2LMHeadModel))
        if os.path.exists(model_dir):
            tokenizer = tokenizer_class.from_pretrained(model_dir)
            model = model_class.from_pretrained(model_dir)
            print(f"Loaded saved model from {model_dir}")
        else:
            tokenizer = tokenizer_class.from_pretrained(self.model_name)
            if self.model_name == 'gpt2':
                tokenizer.pad_token = tokenizer.eos_token  # Set pad token for GPT-2
            model = model_class.from_pretrained(self.model_name)
            model.resize_token_embeddings(len(tokenizer))
            print("No saved model found. Created a new model.")
        return tokenizer, model


# Example usage
def main():
    model_provider = ModelProvider(model_name='gpt2')
    model_dir = './results'
    tokenizer, model = model_provider.load_model(model_dir)
    # Your further processing...


if __name__ == "__main__":
    main()
