from typing import Tuple

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tqdm import tqdm

REAL_TEST_SIZE = 0.2
PATH_TRAIN = 'data/raw_train.csv'
PATH_TEST = 'data/raw_test.csv'


def clean_leak(df_test, df_auth) -> Tuple[pd.DataFrame, pd.DataFrame]:
    counter = dict(zip(df_auth['author_id'], df_auth['n_coauthorship']))
    collect_index_leak = []

    for index in tqdm(df_test.index):
        df_temp = df_test.xs(index)
        auth_1, auth_2 = df_temp['author_id_1'], df_temp['author_id_2']

        if counter[auth_1] == 1 or counter[auth_2] == 1:
            collect_index_leak.append(index)
        else:
            counter[auth_1] -= 1
            counter[auth_2] -= 1

    df_to_train = df_test[df_test.index.isin(collect_index_leak)].copy()
    df_test = df_test.drop(collect_index_leak, axis=0)

    return df_to_train, df_test


PATH_DF_MAIN = 'data/authors_labels.csv'
PATH_AUTH = 'data/auth_and_n_coauth.csv'

df_main = pd.read_csv(PATH_DF_MAIN, sep=',', index_col=None)
df_auth = pd.read_csv(PATH_AUTH, sep=',', index_col=None)

df_auth = df_auth[df_auth['n_coauthorship'] > 1]

set_author = set(df_main['author_id_1']) | set(df_main['author_id_2'])
assert len(set_author - set(df_auth['author_id'])) == 0, \
    'Найдены новые авторы, которых не было в изначальном списке'

df_auth = df_auth[df_auth['author_id'].isin(set_author)]  # некоторые авторы имели соавторство с авторами, у которых
                                                       # данное соавторство было единственным, поэтому они остались
                                                       # по фильтру > 1

assert len(set(df_auth['author_id']) - (set(df_main['author_id_1']) | set(df_main['author_id_2']))) == 0

n_train, n_test = 0, 0
train_header, test_header = True, True

for left, right in [
    (2, 3),
    (4, 6),
    (7, 10),
    (11, 15),
    (16, 32),
    (33, 66),
    (66, 198),
    (199, 317)
]:
    print(left, right)

    df_auth_temp = df_auth[(df_auth['n_coauthorship'] >= left) & (df_auth['n_coauthorship'] <= right)]
    set_author = set(df_auth_temp['author_id'])

    df_temp = df_main[df_main['author_id_1'].isin(set_author) | df_main['author_id_2'].isin(set_author)]

    n_test = int(df_temp.shape[0] * REAL_TEST_SIZE)

    df_train, df_test = train_test_split(df_temp.copy(), test_size=0.3)

    df_to_train, df_real_test = clean_leak(df_test, df_auth)

    df_train = pd.concat([df_train, df_to_train], ignore_index=True)

    if n_test < df_real_test.shape[0]:
        print(f'n_test: {n_test}, n_df_real_test: {df_real_test.shape[0]}')
        df_real_test = df_real_test.sample(frac=1, random_state=42)

        df_to_train = df_real_test[n_test:]
        df_real_test = df_real_test[:n_test]

        df_train = pd.concat([df_train, df_to_train], ignore_index=True)

    df_train.to_csv(PATH_TRAIN, mode='a', sep=',', header=train_header, index=False)
    df_real_test.to_csv(PATH_TEST, mode='a', sep=',', header=test_header, index=False)

    train_header, test_header = False, False

    print(f'Step [{left}, {right}]')
    print(f'Train: {df_train.shape[0]}')
    print(f'Train: {df_real_test.shape[0]}', end='\n' * 2)

    n_train, n_test = n_train + df_train.shape[0], n_test + df_real_test.shape[0]

print(f'Full train/test: {n_train}/{n_test}')
