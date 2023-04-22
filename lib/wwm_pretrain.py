import collections
import numpy as np
import torch
from transformers import (
    BertTokenizerFast,
    BertForMaskedLM,
    DataCollatorForWholeWordMask,
    TrainingArguments,
    Trainer,
)
from datasets import load_dataset, Dataset

device = "mps" if getattr(torch, "has_mps", False) \
    else "gpu" if torch.cuda.is_available() else "cpu"
device = 'cpu'

# Load the dataset
poems = load_dataset("text", data_files="../Raw_data/test_wwm.txt")
poems = poems["train"].train_test_split(test_size=0.1)

class CustomBertTokenizer(BertTokenizerFast):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _tokenize(self, text):
        # Assuming the input text is already a list of pre-tokenized words
        return text

model_name = "hfl/chinese-bert-wwm"
tokenizer = CustomBertTokenizer.from_pretrained(model_name)
model = BertForMaskedLM.from_pretrained(model_name).to(device)

# Tokenize the dataset using whole-word masking
def tokenize_function(examples):
    new_text = []
    for poem in examples:
        poem = poem.strip()
        words = poem.split(" ")
        new
    new_text = []
    for line in text:
        line = line.strip()
        new_text.append(line.split(" "))
    return tokenizer(new_text, return_special_tokens_mask=True)

tokenized_poems = poems.map(tokenize_function, batched=True)
print(tokenized_poems)
# Create a custom Dataset
class CustomDataset(Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}

    def __len__(self):
        return len(self.encodings["input_ids"])

train_dataset = CustomDataset(tokenized_poems["train"])
test_dataset = CustomDataset(tokenized_poems["test"])
print(train_dataset[:2])
# Create a data collator with whole-word masking
data_collator = DataCollatorForWholeWordMask(tokenizer=tokenizer, mlm_probability=0.15)

# Set training arguments
training_args = TrainingArguments(
    output_dir='output',
    overwrite_output_dir=True,
    num_train_epochs=2,
    per_device_train_batch_size=16,
    save_steps=1000,
    save_total_limit=2,
)

# Create a Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
)

# Start training
trainer.train()
