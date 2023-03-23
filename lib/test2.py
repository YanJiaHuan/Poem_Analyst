import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForMaskedLM, AdamW, DataCollatorForLanguageModeling
import time

device = "mps" if getattr(torch,'has_mps',False) \
    else "gpu" if torch.cuda.is_available() else "cpu"
# 1. Load a pre-trained BERT model and tokenizer
model_name = "hfl/chinese-bert-wwm"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForMaskedLM.from_pretrained(model_name).to(device)

# 2. Prepare your dataset of Chinese poems
# poems = ["床前明月光", "疑是地上霜", "举头望明月", "低头思故乡"]  # Replace with your own dataset

file_path = "../Raw_data/chinese_poems.txt"

with open(file_path, "r", encoding="utf-8") as f:
    poems = [line.strip() for line in f.readlines()]
# 3. Tokenize your dataset using the tokenizer
class PoemDataset(Dataset):
    def __init__(self, poems, tokenizer):
        self.poems = poems
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.poems)

    def __getitem__(self, idx):
        poem = self.poems[idx]
        encoding = tokenizer.encode_plus(
            poem,
            add_special_tokens=True,
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=128
        )
        return {key: tensor.squeeze(0) for key, tensor in encoding.items()}

poem_dataset = PoemDataset(poems, tokenizer)
dataloader = DataLoader(poem_dataset, batch_size=256)  # Adjust batch_size based on your available resources

# 4. Fine-tune the BERT model on the MLM task
data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=True, mlm_probability=0.15)

epochs = 3
optimizer = AdamW(model.parameters(), lr=2e-5)


for epoch in range(epochs):
    model.train()
    epoch_start_time = time.time()
    total_loss = 0
    num_batches = 0

    for batch in dataloader:
        batch_start_time = time.time()

        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)

        examples = [{k: v[i] for k, v in batch.items()} for i in range(batch["input_ids"].shape[0])]
        batch = data_collator(examples)

        labels = batch["labels"].to(device)

        optimizer.zero_grad()
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()

        batch_time = time.time() - batch_start_time
        total_loss += loss.item()
        num_batches += 1

        print(f"Epoch {epoch + 1}/{epochs}, Batch {num_batches}: Loss = {loss.item()}, Time = {batch_time:.2f}s")

    epoch_time = time.time() - epoch_start_time
    avg_loss = total_loss / num_batches
    fine_tuned_model_path = "fine_tuned_chinese_bert" + str(epoch)
    tokenizer.save_pretrained(fine_tuned_model_path)
    model.save_pretrained(fine_tuned_model_path)
    print(f"Epoch {epoch + 1}/{epochs}: Average Loss = {avg_loss}, Time = {epoch_time:.2f}s")


# 5. Save the fine-tuned model and tokenizer
fine_tuned_model_path = "fine_tuned_chinese_bert"
tokenizer.save_pretrained(fine_tuned_model_path)
model.save_pretrained(fine_tuned_model_path)
