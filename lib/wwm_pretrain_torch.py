import torch
from transformers import BertTokenizer, BertForMaskedLM, BertModel, BertConfig
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence
import torch.distributed as dist
from sklearn.model_selection import train_test_split
import tqdm
import json
import os

device = "cuda" if torch.cuda.is_available() else "cpu"
model_name = "bert-base-chinese"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForMaskedLM.from_pretrained(model_name)
config = BertConfig.from_pretrained(model_name)
if torch.cuda.device_count() > 1:
    dist.init_process_group(backend='nccl')
    model = torch.nn.DataParallel(model)
model = model.to(device)


with open("../Raw_data/new_chinese_poems_cws.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

poems_data = [{"text": line.strip()} for line in lines]
poems_train, poems_test = train_test_split(poems_data, test_size=0.2, random_state=42)


class PoemsDataset(Dataset):
    def __init__(self, data,limit=None):
        self.data = data[:limit] if limit is not None else data
        # self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        inputs = tokenizer.encode_plus(
            self.data[index]["text"],
            add_special_tokens=True,
            return_attention_mask=True,
            return_tensors="pt",
            max_length=128,
            truncation=True,
        )

        # Apply whole word masking
        inputs_whole_word = tokenizer.prepare_for_model(
            inputs["input_ids"].squeeze().tolist(),
            max_length=128,
            padding="max_length",
            truncation=True,
            return_attention_mask=True,
            return_tensors="pt",
            whole_word_masking=True,
        )
        input_ids = inputs_whole_word["input_ids"].squeeze()
        attention_mask = inputs_whole_word["attention_mask"].squeeze()
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

train_loader = DataLoader(train_dataset, batch_size=128, collate_fn=collate_fn)
eval_loader = DataLoader(eval_dataset, batch_size=128, collate_fn=collate_fn)


# print("Number of samples in the train dataset:", len(train_loader))
# print("Number of samples in the eval dataset:", len(eval_loader))
#
# print("First 5 samples from train dataset:")
# for i in range(5):
#     sample = train_dataset[i]
#     text = tokenizer.decode(sample["input_ids"].tolist(), skip_special_tokens=True)
#     masked_token = tokenizer.decode(sample["input_ids"][sample["masked_indices"]].tolist())
#     print(f"Text: {sample}")
#     print(f"Text: {text}")
#     print(f"Masked token: {masked_token}")
#     print(f"Labels: {sample['labels'].tolist()}")
#     print("=" * 50)

mlm_loss = torch.nn.CrossEntropyLoss(ignore_index=-100)
optimizer = torch.optim.Adam(model.parameters(), lr=2e-5)
epoch_num = 1
for epoch in range(epoch_num):
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
    # evaluation loop
    model.eval()
    total_eval_loss = 0
    with torch.no_grad():
        for batch in tqdm.tqdm(eval_loader):
            outputs = model(
                input_ids=batch["input_ids"],
                attention_mask=batch["attention_mask"],
                labels=batch["labels"],
            )
            loss = mlm_loss(outputs.logits.view(-1, tokenizer.vocab_size), batch["labels"].view(-1))
            total_eval_loss += loss.item()

    avg_eval_loss = total_eval_loss / len(eval_loader)
    print(f"Epoch {epoch + 1} - Average evaluation loss: {avg_eval_loss:.4f}")

    # Save the model and optimizer
    folder_path = "../checkpoints/model_round2/"
    if (epoch + 1) % 1 == 0:
        if isinstance(model, torch.nn.DataParallel):
            model.module.save_pretrained(folder_path)
        else:
            model.save_pretrained(folder_path)

    # Save the logs
    logs = {"epoch": epoch + 1, "avg_train_loss": avg_train_loss, "avg_eval_loss": avg_eval_loss}
    logs_path = f"{folder_path}logs_{epoch + 1}.json"
    with open(logs_path, "w") as f:
        json.dump(logs, f)


# CUDA_VISIBLE_DEVICES=0,1 python -m torch.distributed.launch wwm_pretrain_torch.py
# CUDA_VISIBLE_DEVICES=0,1,2,3 torchrun wwm_pretrain_torch.py