import torch
from transformers import BertTokenizer, BertForMaskedLM
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence
from sklearn.model_selection import train_test_split
import tqdm
import json
import os

device = "cuda" if torch.cuda.is_available() else "cpu"

model_name = "bert-base-chinese"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForMaskedLM.from_pretrained(model_name)

if torch.cuda.device_count() > 1:
    model = torch.nn.DataParallel(model)
model = model.to(device)


with open("../Raw_data/new_chinese_poems_cws.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

poems_data = [{"text": line.strip()} for line in lines]
poems_train, poems_test = train_test_split(poems_data, test_size=0.2, random_state=42)


class PoemsDataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        inputs = tokenizer.encode_plus(
            self.data[index]["text"],
            add_special_tokens=True,
            return_attention_mask=True,
            return_tensors="pt",
            max_length=512,
            truncation=True,
        )
        input_ids = inputs["input_ids"].squeeze()
        attention_mask = inputs["attention_mask"].squeeze()
        masked_indices = torch.where(input_ids == tokenizer.mask_token_id)
        labels = input_ids.clone()
        labels[masked_indices] = -100  # ignore loss for masked tokens
        return {
            "input_ids": input_ids.to(device),
            "attention_mask": attention_mask.to(device),
            "labels": labels.to(device),
            "masked_indices": masked_indices[0].to(device),
        }



def collate_fn(batch):
    input_ids = pad_sequence([data["input_ids"] for data in batch], batch_first=True, padding_value=0)
    attention_mask = pad_sequence([data["attention_mask"] for data in batch], batch_first=True, padding_value=0)
    labels = pad_sequence([data["labels"] for data in batch], batch_first=True, padding_value=-100)
    masked_indices = [data["masked_indices"] for data in batch]
    return {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "labels": labels,
        "masked_indices": masked_indices,
    }


train_dataset = PoemsDataset(poems_train)
eval_dataset = PoemsDataset(poems_test)

train_loader = DataLoader(train_dataset, batch_size=1, collate_fn=collate_fn)
eval_loader = DataLoader(eval_dataset, batch_size=1, collate_fn=collate_fn)

print("Number of samples in the train dataset:", len(train_dataset))
print("Number of samples in the eval dataset:", len(eval_dataset))

print("First 5 samples from train dataset:")
for i in range(5):
    sample = train_dataset[i]
    text = tokenizer.decode(sample["input_ids"].tolist(), skip_special_tokens=True)
    masked_token = tokenizer.decode(sample["input_ids"][sample["masked_indices"]].tolist())
    print(f"Text: {text}")
    print(f"Masked token: {masked_token}")
    print(f"Labels: {sample['labels'].tolist()}")
    print("=" * 50)

mlm_loss = torch.nn.CrossEntropyLoss(ignore_index=-100)
optimizer = torch.optim.Adam(model.parameters(), lr=2e-5)

for epoch in range(2):
    model.train()
    total_loss = 0
    for batch in tqdm.tqdm(train_loader):
        optimizer.zero_grad()
        outputs = model(
            input_ids=batch["input_ids"],
            attention_mask=batch["attention_mask"],
            labels=batch["labels"],
        )
        loss = mlm_loss(outputs.logits.view(-1, tokenizer.vocab_size), batch["labels"].view(-1))
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    avg_train_loss = total_loss / len(train_loader)
    print(f"Epoch {epoch + 1} - Average training loss: {avg_train_loss:.4f}")

    model.eval()
    total_eval_loss = 0
    with torch.no_grad():
        for batch in tqdm.tqdm(eval_loader):
            max_seq_length = 512
            input_ids = batch["input_ids"][0][:max_seq_length]
            attention_mask = batch["attention_mask"][0][:max_seq_length]
            labels = batch["labels"][0][:max_seq_length]

            if len(input_ids) < max_seq_length:
                # Pad input sequence if it is shorter than max_seq_length
                padding_length = max_seq_length - len(input_ids)
                input_ids = torch.cat([input_ids, torch.zeros(padding_length, dtype=torch.long)])
                attention_mask = torch.cat([attention_mask, torch.zeros(padding_length, dtype=torch.long)])
                labels = torch.cat([labels, torch.zeros(padding_length, dtype=torch.long)])

            outputs = model(
                input_ids=input_ids.unsqueeze(0).to(device),
                attention_mask=attention_mask.unsqueeze(0).to(device),
                labels=labels.unsqueeze(0).to(device),
            )

            loss = mlm_loss(outputs.logits.view(-1, tokenizer.vocab_size), batch["labels"].view(-1))
            total_eval_loss += loss.item()
    avg_eval_loss = total_eval_loss / len(eval_loader)
    print(f"Epoch {epoch + 1} - Average evaluation loss: {avg_eval_loss:.4f}")
    # Save the model and optimizer
    if (epoch + 1) % 1 == 0:
        model_path = f"model_{epoch + 1}.pth"
        optimizer_path = f"optimizer_{epoch + 1}.pth"
        torch.save(model.state_dict(), model_path)
        torch.save(optimizer.state_dict(), optimizer_path)

    # Save the logs
    logs = {"epoch": epoch + 1, "avg_train_loss": avg_train_loss, "avg_eval_loss": avg_eval_loss}
    logs_path = f"logs_{epoch + 1}.json"
    with open(logs_path, "w") as f:
        json.dump(logs, f)

## load model
# model = BertForMaskedLM.from_pretrained(model_name).to(device)
# model.load_state_dict(torch.load("model.pth"))
