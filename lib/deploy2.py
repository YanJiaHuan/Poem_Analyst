from transformers import BertTokenizer, BertModel
import torch

device = "mps" if getattr(torch,'has_mps',False) \
    else "gpu" if torch.cuda.is_available() else "cpu"

# Load the fine-tuned model and tokenizer
# fine_tuned_model_path = "fine_tuned_chinese_bert"
fine_tuned_model_path = "hfl/chinese-bert-wwm"
tokenizer = BertTokenizer.from_pretrained(fine_tuned_model_path)
model = BertModel.from_pretrained(fine_tuned_model_path).to(device)

# Define a function to get the word embeddings
def get_word_embeddings(text, tokenizer, model):
    input_ids = tokenizer.encode(text, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(input_ids)
        embeddings = outputs.last_hidden_state
    return embeddings.cpu().numpy()

text = []
with open('../Raw_data/new_chinese_poems_cws.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        text.append(line.strip())

# Use the fine-tuned model to obtain word embeddings for a given text
# text = "床前明月光，疑是地上霜，举头望明月，低头思故乡"
# text = '我喜欢吃苹果，小明是个人'
embeddings = get_word_embeddings(text, tokenizer, model)

print(f"Text: {text}")
print(f"Embeddings shape: {embeddings.shape}")
print(f"Embeddings: {embeddings}")
# for word in text:
#     print(f"tokenizerd:{tokenizer.tokenize(word)}")
