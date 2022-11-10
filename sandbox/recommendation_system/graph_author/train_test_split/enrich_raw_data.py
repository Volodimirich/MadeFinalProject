import json

import pandas as pd
import ujson
from tqdm import tqdm

PATH_DF = r'D:\projects\hm\made_project_semestr_1\id_class_clean.csv'

df = pd.read_csv(PATH_DF, sep=',', index_col=None, header=0)

id_to_label = dict(zip(df['_id'], df['label']))

print('n: ', len(id_to_label))

N_CHUNK = 50_000
PATH_RAW_DATA = '../dblpv13.jsonl'
PATH_ENRICHED_RAW_DATA = 'data/dblpv13_w_class.jsonl'

n = 0
with open(PATH_RAW_DATA, 'r', encoding='utf-8') as fio, open(PATH_ENRICHED_RAW_DATA, 'w', encoding='utf-8') as fio_cls:
    for line in tqdm(fio):
        dict_line = ujson.loads(line)

        label = id_to_label.get(dict_line['_id'])

        if label is not None:
            n += 1

            dict_line['label'] = label

            fio_cls.write(json.dumps(dict_line) + '\n')

print('n: ', n)
