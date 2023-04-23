import random
import torch
from torch.utils.data import Dataset, DataLoader
import pytorch_lightning as pl
import pandas as pd
import re


def remove_all_punkt(text):
    """
    Removes all punctuation from Chinese text.

    :param text: text to remove punctuation from
    :return: text with no punctuation
    """
    return re.sub(r'[^\w\s]', '', text)


class Seq2Seq(Dataset):
    def __init__(
        self, df, tokenizer, target_tokenizer,
        max_len=128,
        no_punkt: bool = False,
    ):
        """
        no_punkt, do we ramdomly remove punctuation
        from source sentence
        """
        super().__init__()
        self.df = df
        self.tokenizer = tokenizer
        self.target_tokenizer = target_tokenizer
        self.max_len = max_len
        self.no_punkt = no_punkt

    def __len__(self, ):
        return len(self.df)

    def __getitem__(self, idx):
        return dict(self.df.iloc[idx])

    def collate(self, batch):
        batch_df = pd.DataFrame(list(batch))
        x, y = batch_df.source, batch_df.target
        # there is a random no punctuation mode
        # for source text
        # as some of the classical text we get
        # might be whole chunk of paragraph without
        # any punctuation
        if self.no_punkt:
            x = list(i if random.random() > .5
                     else remove_all_punkt(i)
                     for i in x)
        else:
            x = list(x)
        x_batch = self.tokenizer(
            x,
            max_length=self.max_len,
            padding='max_length',
            truncation=True,
            return_tensors='pt',
        )
        y_batch = self.target_tokenizer(
            list(y),
            max_length=self.max_len,
            padding='max_length',
            truncation=True,
            return_tensors='pt',
        )
        x_batch['decoder_input_ids'] = y_batch['input_ids']
        x_batch['labels'] = y_batch['input_ids'].clone()
        x_batch['labels'][x_batch['labels'] ==
                          self.tokenizer.pad_token_id] = -100
        return x_batch

    def dataloader(self, batch_size, shuffle=True):
        return DataLoader(
            self,
            batch_size=batch_size,
            shuffle=shuffle,
            collate_fn=self.collate,
        )

    def split_train_valid(self, valid_size=0.1):
        split_index = int(len(self) * (1 - valid_size))
        cls = type(self)
        shuffled = self.df.sample(frac=1).reset_index(drop=True)
        train_set = cls(
            shuffled.iloc[:split_index],
            tokenizer=self.tokenizer,
            target_tokenizer=self.target_tokenizer,
            max_len=self.max_len,
            no_punkt=self.no_punkt,
        )
        valid_set = cls(
            shuffled.iloc[split_index:],
            tokenizer=self.tokenizer,
            target_tokenizer=self.target_tokenizer,
            max_len=self.max_len,
            no_punkt=self.no_punkt,
        )
        return train_set, valid_set


"""### PL datamodule"""


class Seq2SeqData(pl.LightningDataModule):
    def __init__(
            self, df,
            tokenizer,
            target_tokenizer,
            batch_size=12,
            max_len=128,
            no_punkt: bool = False):
        super().__init__()
        self.df = df
        self.ds = Seq2Seq(df,
                          tokenizer,
                          target_tokenizer,
                          max_len=max_len,
                          no_punkt=no_punkt)
        self.tokenizer = tokenizer
        self.target_tokenizer = target_tokenizer
        self.max_len = max_len
        self.batch_size = batch_size

    def setup(self, stage=None):
        self.train_set, self.valid_set = self.ds.split_train_valid()

    def train_dataloader(self):
        return self.train_set.dataloader(
            batch_size=self.batch_size, shuffle=True)

    def val_dataloader(self):
        return self.valid_set.dataloader(
            batch_size=self.batch_size*2, shuffle=False)


class Seq2SeqTrain(pl.LightningModule):
    def __init__(self, encoder_decoder):
        super().__init__()
        self.encoder_decoder = encoder_decoder

    def forward(self, batch):
        return self.encoder_decoder(
            **batch
        )

    def training_step(self, batch, batch_idx):
        outputs = self(batch)
        self.log('loss', outputs.loss)
        return outputs.loss

    def validation_step(self, batch, batch_idx):
        outputs = self(batch)
        self.log('val_loss', outputs.loss)
        return outputs.loss

    def configure_optimizers(self):
        encoder_params = list(
            {"params": param, "lr": 1e-5}
            for param in self.encoder_decoder.encoder.embeddings.parameters()) +\
            list({"params": param, "lr": 1e-5}
                 for param in self.encoder_decoder.encoder.encoder.parameters()) +\
            list({"params": param, "lr": 1e-3}
                 for param in self.encoder_decoder.encoder.pooler.parameters())

        decoder_params = list()
        for name, param in self.encoder_decoder.decoder.named_parameters():
            if 'ln_cross_attn' in name:
                decoder_params.append({"params": param, "lr": 1e-3})
            elif 'crossattention' in name:
                decoder_params.append({"params": param, "lr": 1e-3})
            elif 'lm_head' in name:
                decoder_params.append({"params": param, "lr": 1e-4})
            else:
                decoder_params.append({"params": param, "lr": 1e-5})

        return torch.optim.Adam(
            encoder_params + decoder_params,
            lr=1e-3,
        )
