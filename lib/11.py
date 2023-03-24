from ltp import LTP
ltp = LTP() # 默认加载 LTP/Small 模型
# ltp = LTP(path = "LTP/base|LTP/small|LTP/tiny")

words = ltp.pipeline(["床前明月光，疑是地上霜，举头望明月，低头思故乡"], tasks = ["cws"], return_dict = False)
print(words)