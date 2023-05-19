from tqdm import tqdm
from pathlib import Path
import pandas as pd


def load_data_for_train(path_data, TO_CLASSICAL):
    DATA = Path(path_data)

    # load 路径下 所有data文件夹下的文件
    all_file = list(DATA.rglob("data/*"))

    print(f"\n load all file: {all_file}")

    def open_file_to_lines(file):
        with open(file) as f:
            lines = f.read().splitlines()
        return lines

    def pairing_the_file(files, kw):
        pairs = []
        for file in files:
            if kw not in file.name:
                file1 = file
                file2 = f"{file}{kw}"
                pairs.append((file1, file2))
        return pairs

    # data 下的所有文件夹格式 - [data; data翻译]
    pairs = pairing_the_file(all_file, "翻译")

    def open_pairs(pairs):
        chunks = []
        for pair in tqdm(pairs, leave=False):
            file1, file2 = pair
            lines1 = open_file_to_lines(file1)
            if len(lines1) > 10:
                lines1 = lines1[:10]
            lines2 = open_file_to_lines(file2)
            if len(lines2) > 10:
                lines2 = lines2[:10]
            chunks.append(pd.DataFrame({"classical": lines1, "modern": lines2}))
        return pd.concat(chunks).sample(frac=1.).reset_index(drop=True)

    data_df = open_pairs(pairs)

    print(f'\n data_df: \n{data_df}')

    df = data_df.rename(
        columns=dict(
            zip(["modern", "classical"],
                ["source", "target"] if TO_CLASSICAL else ["target", "source", ]))
    )

    print(f'\n{df.head(5)}')

    return df
