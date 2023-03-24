from ltp import LTP
# import time

ltp = LTP() # 默认加载 LTP/Small 模型
# ltp = LTP(path = "LTP/base|LTP/small|LTP/tiny")
# read text in chinses_poem.txt line by line,and save in a new txt file
new_text = []

with open('../Raw_data/chinese_poems.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # start_time = time.time()
        word = ltp.pipeline(line, tasks=["cws"], return_dict=False)
        new_text.append(word)
        # end_time = time.time()
        # print(end_time-start_time)
print(new_text)
# write into a new text file
with open('../Raw_data/new_chinese_poems_cws.txt', 'w', encoding='utf-8') as f:
    for line in new_text:
        f.write(' '.join(line[0]))
        f.write('\n')




