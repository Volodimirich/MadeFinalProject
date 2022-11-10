from collections import defaultdict

import pandas as pd
import ujson
from tqdm import tqdm

N_CHUNK = 50_000
PATH_RAW_DATA = 'data/dblpv13_w_class.jsonl'
PATH_AUTH_COAUTH = 'data/auth_and_n_coauth.csv'
PATH_TO_SAVE_DATAFRAME = 'data/authors_year_label_not_grouped.csv'

dict_author_id = defaultdict(int)

with open(PATH_RAW_DATA, 'r', encoding='utf-8') as fio:
    i = 0
    data_for_df = {
        'author_id_1': [],
        'author_id_2': [],
        'year': [],
        'label': [],
        'article_id': []
    }
    header = True

    for line in tqdm(fio):
        i += 1

        dict_line: dict = ujson.loads(line)

        article_id = dict_line['_id']
        year = dict_line.get('year')
        label = dict_line['label']
        list_author = dict_line.get('authors', [])

        for i, dict_author_1 in enumerate(list_author):
            author_id_1 = dict_author_1.get('_id')

            if author_id_1 is None:
                continue

            for dict_author_2 in list_author[i + 1:]:
                author_id_2 = dict_author_2.get('_id')

                if author_id_2 is None:
                    continue

                sorted_auth_1, sorted_auth_2 = sorted([author_id_1, author_id_2])

                data_for_df['author_id_1'].append(sorted_auth_1)
                data_for_df['author_id_2'].append(sorted_auth_2)
                data_for_df['year'].append(year)
                data_for_df['label'].append(label)
                data_for_df['article_id'].append(article_id)

        if i % N_CHUNK == 0:
            df_chunk = pd.DataFrame(data_for_df)
            df_chunk.to_csv(PATH_TO_SAVE_DATAFRAME, mode='a', sep=',', header=header, index=False)

            header = False

            del df_chunk
            del data_for_df

            data_for_df = {
                'author_id_1': [],
                'author_id_2': [],
                'year': [],
                'label': [],
                'article_id': []
            }

if len(data_for_df['author_id_1']) > 0:
    df_chunk = pd.DataFrame(data_for_df)
    df_chunk.to_csv(PATH_TO_SAVE_DATAFRAME, mode='a', sep=',', header=header, index=False)
