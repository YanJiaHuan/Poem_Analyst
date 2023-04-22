import torch
from transformers import (
    BertTokenizer,
    BertForMaskedLM,
    DataCollatorForWholeWordMask,
    TrainingArguments,
    Trainer,
)
from datasets import load_dataset, Dataset

device = "mps" if getattr(torch, "has_mps", False) \
    else "gpu" if torch.cuda.is_available() else "cpu"

model_name = "bert-base-chinese"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForMaskedLM.from_pretrained(model_name).to(device)

with open("../Raw_data/test_wwm.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

poems_data = [{"text": line.strip()} for line in lines]
poems = Dataset.from_dict({"text": [d["text"] for d in poems_data]})
poems = poems.shuffle(seed=42)
poems = poems.train_test_split(test_size=0.2)



train_dataset = poems["train"]
eval_dataset = poems["test"]

print("Number of samples in the train dataset:", len(train_dataset))
print("Number of samples in the eval dataset:", len(eval_dataset))

print("First 5 samples from train dataset:")
for i in range(len(train_dataset)):
    print(train_dataset[i])

data_collator = DataCollatorForWholeWordMask(tokenizer=tokenizer, mlm_probability=0.15)

training_args = TrainingArguments(
    output_dir='output',
    overwrite_output_dir=True,
    num_train_epochs=2,
    per_device_train_batch_size=1,
    save_steps=1000,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
)

trainer.train()
