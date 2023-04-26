from transformers import BertTokenizer
import os
from pathlib import Path
import torch
from datasets import load_dataset
from transformers import BertModel, AdamW
from torch.utils.data import Dataset, DataLoader



script_dir = os.path.dirname(os.path.abspath(__file__))
train_dir = script_dir + '\\text.json'
test_dir = script_dir + '\\test.json'

dataset_train = load_dataset('json', data_files=train_dir, split="train", field='data')
dataset_test = load_dataset('json', data_files=test_dir, split="train", field='data')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# 拆分每首诗的句子成为单独的样本
train_texts_1 = []
train_texts_2 = []
train_labels=[]
for data in dataset_train:
    train_texts_1.append(data["target_sentence"])
    train_texts_2.append(data["candidate_allusion"])
    train_labels.append(data['label'])

test_texts_1 = []
test_texts_2 = []
test_labels = []
for data in dataset_test:
    test_texts_1.append(data["target_sentence"])
    test_texts_2.append(data["candidate_allusion"])
    test_labels.append(data['label'])


tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
train_encodings = tokenizer(train_texts_1,train_texts_2, truncation=True, padding=True)
test_encodings = tokenizer(test_texts_1,test_texts_2, truncation=True, padding=True)


class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = Dataset(train_encodings, train_labels)
test_dataset = Dataset(test_encodings, test_labels)


#生成训练和测试Dataloader
train_loader = DataLoader(train_dataset, batch_size=1, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=True)


class myFinrtuneModel(torch.nn.Module):
    def __init__(self,model_name='bert-base-chinese',freeze_bert=False):
        super(myFinrtuneModel,self).__init__()
        # bert模型
        self.bert = BertModel.from_pretrained(model_name)
        if freeze_bert:
            for p in self.bert.parameters():
                p.requires_grad=False
        # 定义bert后面要接的网络
        self.class_net = torch.nn.Linear(768,1)

    # 微调的具体操作
    def forward(self,input_ids,attention_masks):
        # 输入bert
        outputs = self.bert(input_ids, attention_mask=attention_masks)
        # 获取bert输出的隐藏层特征
        last_hidden_state=outputs.last_hidden_state
        # 把token embedding平均得到sentences_embedding
        sentences_embeddings=torch.mean(last_hidden_state,dim=1)
        sentences_embeddings=sentences_embeddings.squeeze(1)
        # 把sentences_embedding输入分类网络
        out=self.class_net(sentences_embeddings).squeeze(-1)
        return out

model=myFinrtuneModel(model_name='bert-base-chinese')

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model.to(device)

model.train()
optim = AdamW(model.parameters(), lr=5e-5)
max_epoch=3
loss_function=torch.nn.BCEWithLogitsLoss()


def save(model,optimizer,PATH):
    my_file = Path(PATH)
    if not my_file.exists():
        os.system("mkdir "+PATH)
    torch.save({
        'model_state_dict':model.state_dict(),
        'optimizer_state_dict':optimizer.state_dict()
    },os.path.join(PATH, 'checkpoint-ep3-e5'))
    print("保存模型参数")

def train(model,train_loader,test_loader,optim,loss_function,max_epoch):
    print('-------------- start training ---------------','\n')
    step=0
    for epoch in range(max_epoch):
        print("========= epoch:",epoch,'==============')
        for batch in train_loader:
            step+=1
            # 清空优化器
            optim.zero_grad()

            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            # 将用例输入模型，计算loss
            out=model(input_ids=input_ids,attention_masks=attention_mask)
            loss=loss_function(out,labels)

            if step%100==0:
                print('step ',step,"loss:",format(loss.item(),'.3f'))

            # 反向传播
            loss.backward()
            optim.step()

        # 每一次epoch进行一次测试
        eval(model=model,test_loader=test_loader)

def eval(model,test_loader):
    right=0
    total=0
    for batch in test_loader:
        total+=1

        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)

        out=torch.sigmoid(model(input_ids=input_ids,attention_masks=attention_mask))
        # 二分类
        pred_label=0 if out.item()<=0.5 else 1
        if pred_label == labels.item():
            right+=1

    accurcy=format(right/total, '.3f')
    print("= accurcy:",accurcy)
    print("\n")

# train(model=model,train_loader=train_loader,test_loader=test_loader,optim=optim,loss_function=loss_function,max_epoch=max_epoch)
# save(model,optim,'save_BertModel_for_text_similarity')
