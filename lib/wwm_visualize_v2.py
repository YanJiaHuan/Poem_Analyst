import torch
import numpy as np
from sklearn.manifold import TSNE
from transformers import BertForMaskedLM, BertTokenizer
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import os
output_dir = "../output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)



device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_name = "bert-base-chinese"
# model_name = "../checkpoints/model_round2/"
model = BertForMaskedLM.from_pretrained(model_name).to(device)
tokenizer = BertTokenizer.from_pretrained(model_name)
#
# # Load the saved model parameters
# saved_model_path = "../checkpoints/model_1.pth"
# saved_state = torch.load(saved_model_path, map_location=device)
#
# # Apply the loaded state to the new model instance
# model.load_state_dict(saved_state)
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

def draw_lines_between_pairs(ax, X_2d, word_pairs):
    for idx1, idx2 in word_pairs:
        x1, y1 = X_2d[idx1]
        x2, y2 = X_2d[idx2]
        ax.plot([x1, x2], [y1, y2], linestyle=':', color='blue', linewidth=1, alpha=0.6)


word_list = ["苹","果","香","蕉","西","瓜","手","机","子","孙","惆","怅","狂","风","猛","雨","凤","凰","周","庄","梦","蝶","浮","生","故","乡","社","燕","松","萝","琉","璃","范","蠡","金","鼎","轩","辕","故","人","红","霞"]  # replace with actual words
embedding_list = extract_embeddings(model, tokenizer, word_list)

tsne = TSNE(n_components=2, perplexity=8, random_state=42)
X_2d = tsne.fit_transform(embedding_list)

fig, ax = plt.subplots(figsize=(12, 12))
plt.rc("font", family='PingFang HK')
plt.scatter(X_2d[:, 0], X_2d[:, 1],c='red', alpha=0.6, s=100)

for i, word in enumerate(word_list):
    plt.annotate(word, xy=(X_2d[i, 0], X_2d[i, 1]), xytext=(2, 2), textcoords='offset points', fontsize=12)

word_pairs = [(0, 1), (2, 3), (4, 5),(6,7),(8,9),(10,11),(12,13),(14,15),(16,17),(18,19),(20,21),(22,23),(24,25),(26,27),(28,29),(30,31),(32,33),(34,35),(36,37),(38,39),(40,41)]  # Replace with actual indices of word pairs


draw_lines_between_pairs(ax, X_2d, word_pairs)

plt.xlabel('t-SNE dimension 1')
plt.ylabel('t-SNE dimension 2')
plt.title('t-SNE visualization of word embeddings with distance lines')

# Save the graph in the "output" folder
plt.savefig(os.path.join(output_dir, 'tsne_bert.png'))

plt.show()


