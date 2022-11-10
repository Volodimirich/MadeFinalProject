import pandas as pd

PATH_TRAIN_FROM = 'data/raw_train.csv'
PATH_TRAIN_TO = 'train_test/train.csv'
PATH_TEST_FROM = 'data/raw_test.csv'
PATH_TEST_TO = 'train_test/test.csv'

for path_from, path_to in [
    (PATH_TRAIN_FROM, PATH_TRAIN_TO),
    (PATH_TEST_FROM, PATH_TEST_TO)
]:
    df = pd.read_csv(path_from, sep=',', index_col=None, header=0)

    df_new = df.copy()
    df_new['author_id_1'], df_new['author_id_2'] = df_new['author_id_2'], df_new['author_id_1']

    df = pd.concat([df, df_new], ignore_index=True)

    df.to_csv(path_to, sep=',', index=False)
