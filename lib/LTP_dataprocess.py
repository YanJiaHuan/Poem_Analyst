from multiprocessing import Pool, freeze_support
from ltp import LTP

def process_line(line):
    return ltp.pipeline(line, tasks=["cws"], return_dict=False)
# new_line = ltp.pipeline(line, tasks=["cws"], return_dict=False)

ltp = LTP()
pool = None

if __name__ == '__main__':
    freeze_support()

    with open('../Raw_data/chinese_poems.txt', 'r', encoding='utf-8') as fin, \
         open('../Raw_data/output.txt', 'w', encoding='utf-8') as fout:
        # Use a multiprocessing.Pool to process lines in parallel
        pool = Pool()

        # Use a generator expression to process lines in batches
        for batch_idx, batch in enumerate(iter(lambda: list(fin)[:1000], [])):
            processed_lines = pool.map(process_line, batch)

            # Write the processed lines to the output file
            for line in processed_lines:
                fout.write(' '.join(line) + '\n')

            print(f'Processed batch {batch_idx} of {len(batch)} lines')

        pool.close()
