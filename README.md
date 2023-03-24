# Poem_Analyst
This is a course project from NUS-ISS about Practical Language Processing. We are dedicated to help 
poem(especially chinese poem) lovers to better understand the imagery, emotion, events mentioned in poems.

![img.png|500](Image/img.png)

<font face="黑体" color=black size=6>一些想法：</font>

古诗词有比较特殊的文本结构，通常的word embedding不太能够正确表示，需要在bert-wwm上重新预训练

古诗词的tokenizer需要把特殊的意象，事件分词，避免切分意象

在这基础上，有两个分支，可以做知识图谱+图像生成，或者白话翻译+图像生成

## ==安装huggingface==
conda install -c huggingface transformers
这个得在pytorch或者tensorflow支持下运行
根据自己电脑去https://pytorch.org/get-started/locally/安装pytorch
conda install pytorch torchvision torchaudio -c pytorch

## ==mac 装torch with GPU==
link：https://www.youtube.com/watch?v=VEDy-c5Sk8Y

## == weights you might want to use==
https://drive.google.com/drive/folders/1D0K5npxx9PBsHhMe5y8fmXoAz7mOUXgx?usp=sharing

## ==LTP==
pip install ltp
link: https://ltp.ai/docs/quickstart.html#id6