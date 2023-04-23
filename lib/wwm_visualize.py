import torch
import numpy as np
from sklearn.manifold import TSNE
from transformers import BertForMaskedLM, BertTokenizer
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm



device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_name = "bert-base-chinese"
model = BertForMaskedLM.from_pretrained(model_name).to(device)
tokenizer = BertTokenizer.from_pretrained(model_name)

# Load the saved model parameters
saved_model_path = "../checkpoints/model_1.pth"
saved_state = torch.load(saved_model_path, map_location=device)

# Apply the loaded state to the new model instance
model.load_state_dict(saved_state)
model.eval()  # Set the model to evaluation mode

def extract_embeddings(model, tokenizer, words):
    embeddings = []
    for word in words:
        inputs = tokenizer(word, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = model(**inputs)
        embeddings.append(outputs[0][0, 1:-1].mean(dim=0).cpu().numpy())
    return np.vstack(embeddings)

word_list = ["床","明","光","须","臾","百","云","藓","痕","子","孙","惆","怅","狂","风","猛","猛雨","凤","凰","明月","周","撞","梦","蝶","浮","生"]  # replace with actual words
embedding_list = extract_embeddings(model, tokenizer, word_list)

tsne = TSNE(n_components=2, perplexity=20, random_state=42)
X_2d = tsne.fit_transform(embedding_list)
plt.figure(figsize=(12, 12))
plt.rc("font",family='PingFang HK')
plt.scatter(X_2d[:, 0], X_2d[:, 1])

for i, word in enumerate(word_list):
    plt.annotate(word, xy=(X_2d[i, 0], X_2d[i, 1]), xytext=(2, 2), textcoords='offset points', fontsize=12)

plt.xlabel('t-SNE dimension 1')
plt.ylabel('t-SNE dimension 2')
plt.title('t-SNE visualization of word embeddings')
plt.show()
