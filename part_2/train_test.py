# -*- coding: utf-8 -*-
"""
Dataset: https://github.com/BangBOOM/Classical-Chinese
"""

import torch
import torch.nn as nn
from load_data import *
from model import *
from transformers import (
    BertModel, BertTokenizer, BertConfig,
    AutoModel, AutoTokenizer,
    EncoderDecoderModel
)
import pytorch_lightning as pl

"""
Set your path
path_data： "_path/data/所有的data文件"   _path 的部分作为 path_data
path_checkpoint： "_path/checkpoint"    _path/checkpoint 的部分作为 path_checkpoint
path_checkpoint_best： 想要验证的模型(.ckpt 文件) 例如 - "/content/gdrive/MyDrive/nlp_project/yuan-main/checkpoint/epoch=1-step=3178.ckpt"
"""
path_data = "../Raw_data"
path_checkpoint = "../checkpoints/Translation"
# path_checkpoint_best = "../checkpoints/Translation"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
"""## Config"""

TO_CLASSICAL = False
df = load_data_for_train(path_data, TO_CLASSICAL)


"""### Loading tokenizer"""
# Pre-trained models
ENCODER_PRETRAINED = "bert-base-chinese"
DECODER_PRETRAINED = "uer/gpt2-chinese-poem"

# Load the saved model parameters
save_model_path = "../checkpoints/model_5.pth"

# Initialize the encoder and decoder
encoder = BertModel.from_pretrained(ENCODER_PRETRAINED)
decoder = AutoModel.from_pretrained(DECODER_PRETRAINED)

# Load the saved state into the encoder
saved_state = torch.load(save_model_path, map_location='cpu')
fixed_state = {k.replace("module.bert.", ""): v for k, v in saved_state.items()}
encoder.load_state_dict(fixed_state)

encoder_after  = encoder.bert
# Add a pooler layer if it's missing
config = BertConfig.from_pretrained(ENCODER_PRETRAINED)
if not hasattr(encoder_after, 'pooler'):
    encoder_after.pooler = nn.Sequential(
        nn.Linear(config.hidden_size, config.hidden_size),
        nn.Tanh()
    )

# Use the extracted BERT model as an encoder for your downstream tasks
encoder_after = encoder_after.to(device)

# Initialize the tokenizer
encoder_tokenizer = BertTokenizer.from_pretrained(ENCODER_PRETRAINED)
decoder_tokenizer = AutoTokenizer.from_pretrained(DECODER_PRETRAINED)

"""### Pytoch Dataset"""

data_module = Seq2SeqData(
    df, encoder_tokenizer,
    decoder_tokenizer,
    batch_size=32,
    max_len=256,
    no_punkt=False if TO_CLASSICAL else True,)
data_module.setup()

inputs = next(iter(data_module.train_dataloader()))
print(f'\ninputs:\n{inputs}')

test = next(iter(data_module.val_dataloader()))
print(f'\ntest:\n{test}')


"""if we are doing clasical Chinese to modern Chinese, we can randomly set half of the input without any punctuation, 
as many data source might be """

encoder_tokenizer.batch_decode(
    inputs.input_ids, skip_special_tokens=True
)

"""### Load pretrained models"""

# encoder = AutoModel.from_pretrained(ENCODER_PRETRAINED, proxies={"http":"bifrost:3128"})
# decoder = AutoModelForCausalLM.from_pretrained(DECODER_PRETRAINED, add_cross_attention=True,
#                                                proxies={"http":"bifrost:3128"})

"""## Model

We create a seq2seq model by using pretrained encoder + pretrained decoder
"""

# loading pretrained model
# encoder_decoder = EncoderDecoderModel.from_encoder_decoder_pretrained(
#     encoder_pretrained_model_name_or_path=encoder,
#     decoder_pretrained_model_name_or_path=DECODER_PRETRAINED,
# )
encoder_decoder = EncoderDecoderModel(encoder=encoder_after, decoder=decoder)

module = Seq2SeqTrain(encoder_decoder)

"""## Training"""

save = pl.callbacks.ModelCheckpoint(
    path_checkpoint,
    save_top_k=1,
    verbose=True,
    monitor='val_loss',
    mode='min',
)

trainer = pl.Trainer(
    # devices=-1,
    max_epochs=10,
    callbacks=[save],
)


# trainer.fit(module, datamodule=data_module)


# test

# print(f"Best model path: {save.best_model_path}")
#
# module.load_state_dict(
#     torch.load(str(path_checkpoint_best), map_location="cpu")['state_dict'])
# 如果有 train 完的话，用下面这个代码 导入 beat model
# module.load_state_dict(
#     torch.load(str(save.best), map_location="cpu")['state_dict'])

model = encoder_decoder
model = model.cpu()
model = model.eval()

# model.save_pretrained(hub/"kw-lead-po")

# model.push_to_hub("raynardj/keywords-cangtou-chinese-poetry")

tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")


def inference(lead):
    leading = f"《{lead}》"
    input_ids = tokenizer(leading, return_tensors='pt', ).input_ids
    # print(tokenizer.sep_token_id)
    with torch.no_grad():
        pred = model.generate(
            input_ids,
            max_length=128,
            num_beams=4,
            #             do_sample=True,
            #             top_p=.6,
            bos_token_id=tokenizer.sep_token_id,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.sep_token_id,
        )
    print(pred)
    return tokenizer.batch_decode(pred, skip_special_tokens=True)

inf = inference('又且驱迫邮传，征求饩廪，折辱州县，闭偿逋负，至仓之日，变鬻以归。官司交忿，农民窘窜。')
# inf = inference('"梦蝶"是一个源自中国哲学家庄子的典故')
print("*"*20)
print(inf)


# CUDA_VISIBLE_DEVICES=0 python train_test.py

# scp -r jiahuan@10.2.56.139:/home/jiahuan/test/poem/checkpoints/model_5.pth /Users/alinlp/PycharmProjects/Poem_Analyst/