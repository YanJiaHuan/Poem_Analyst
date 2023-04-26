import json
import os
import torch
from transformers import AutoTokenizer, AutoModel
from train_1 import myFinrtuneModel

# 获取当前脚本所在路径
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = script_dir + '\my_file.json'
# result_dir = script_dir + '\\test.json'
checkpoints = script_dir + '\checkpoint -ep1-e6'

# 加载预训练的BERT模型和对应的分词器
model_name = 'bert-base-chinese'
# # model_name = 'hfl/chinese-bert-wwm'
tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModel.from_pretrained(model_name)

# 定义两个文本
target_sentence = "织锦制回文诗，以赎夫罪。"
# "小园芳草绿，家住越溪曲。"
with open(data_dir, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 将key和value分别存储到两个列表中
sentences = []
values = []
for k, v in data.items():
    sentences.append(k)
    values.append(v)

# # 对目标句子进行编码
# target_tokens = tokenizer.encode(target_sentence, add_special_tokens=True, return_tensors="pt")
#
# # 对10个句子进行编码并计算相似度
# similarities = []
# for sentence in sentences:
#     # 对句子进行编码
#     tokens = tokenizer.encode(sentence, add_special_tokens=True, return_tensors="pt")
#
#     # 使用BERT模型计算相似度
#     with torch.no_grad():
#         target_output = model(target_tokens)[0][:, 0, :]
#         output = model(tokens)[0][:, 0, :]
#         cosine_similarity = torch.nn.functional.cosine_similarity(target_output, output).item()
#         similarities.append(cosine_similarity)
#
# # 输出相似度最高的两个句子
# top_similarities = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)[:10]
# print(f"Target poem: {target_sentence}")
# i = 1
# for idx, sim in top_similarities:
#     # print(f"Similarity with sentence {idx + 1}: {sim:.3f}")
#     # print(f"Allusion {idx + 1}: {sentences[idx]}   {sim:.3f}")
#     print(f"Allusion {i}: {sentences[idx]}   {sim:.3f}")
#     i += 1


# 加载预训练的BERT模型和对应的分词器
# model_name = 'bert-base-chinese'
# model_name = 'hfl/chinese-bert-wwm'
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModel.from_pretrained(model_name)
checkpoint = torch.load(checkpoints)
model = myFinrtuneModel()
model.load_state_dict(checkpoint['model_state_dict'])


# model.eval()

# 对10个句子进行编码并计算相似度
similarities = []
for sentence in sentences:
    # 对句子进行编码
    tokens = tokenizer(sentence, target_sentence, return_tensors="pt")
    input_ids = tokens['input_ids']
    attention_mask = tokens['attention_mask']
    # 使用BERT模型计算相似度
    outputs = model(input_ids=input_ids, attention_masks=attention_mask)
    outputs = torch.sigmoid(outputs).item()
    similarities.append(outputs)

# 输出相似度最高的两个句子
top_similarities = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)[:10]
print(top_similarities)
print(f"Target poem: {target_sentence}")
i = 1
L = []
for idx, sim in top_similarities:
    # print(f"Similarity with sentence {idx + 1}: {sim:.3f}")
    # print(f"Allusion {idx + 1}: {sentences[idx]}   {sim:.3f}")
    string_ = 'Allusion ' + str(i) + ': ' + str(sentences[idx]) + '    ' + str(round(sim, 3))
    L.append(string_)

    print(f"Allusion {i}: {sentences[idx]}   {sim:.3f}")
    i += 1

print(L)




#
# with open(data_dir, 'r', encoding='utf-8') as f:
#     data = json.load(f)
#
# notes_list = [] # 存储所有notes
# paragraphs_list = []
# for item in data:
#     notes_list.extend(item['notes'])  # 将每个item中的notes添加到notes_list中
#     paragraphs_list.extend(item['paragraphs'])
# print(paragraphs_list)
#
# words_list = []
# for item in notes_list:
#     try:
#         parts = item.split(".", 1)  # 以数字序号为分隔符，最多分割 1 次
#         key = parts[1].split("--")[0]  # 以连词符为分隔符，取前面的文本
#         words_list.append(key)
#         # value = parts[1].split("--")[1]  # 以连词符为分隔符，取后面的文本
#         # result_dict[key] = value
#     except:
#         print(f"Error: Unable to process data - {item}")
#
# print(words_list)
# import random
# dataset2 = []
# for words in words_list:
#     candidate_allusion = words
#     for para in paragraphs_list:
#         if words in para:
#             target_sentence = para
#             label = 1.0
#             dataset2.append({
#                 'target_sentence': target_sentence,
#                 'candidate_allusion': candidate_allusion,
#                 'label': label
#             })
#             n = len(paragraphs_list)
#             i = random.randint(0, n - 1)
#
#             target_sentence = paragraphs_list[i]
#             label = 0.0
#             dataset2.append({
#                 'target_sentence': target_sentence,
#                 'candidate_allusion': candidate_allusion,
#                 'label': label
#             })
#
# print(dataset2)
# #
# #
# #
# # # 写入文件，以追加模式打开文件
# with open(result_dir, 'a', encoding='utf-8') as f:
#     json.dump(dataset2, f, ensure_ascii=False, indent=4)
