import pandas as pd

PATH_DF_MAIN = 'data/authors_year_label_not_grouped.csv'
PATH_DF_AUTH_COAUTH = 'data/auth_and_n_coauth.csv'
PATH_TO_SAVE_DF_AUTHORS_LABELS = 'data/authors_labels.csv'

df_main = pd.read_csv(PATH_DF_MAIN, sep=',', index_col=None, header=0)
df_auth = pd.read_csv(PATH_DF_AUTH_COAUTH, sep=',', index_col=None, header=0)

print(df_main.shape)  # (2826076, 5)

set_author_id = set(df_auth[df_auth['n_coauthorship'] > 1]['author_id'])
print(len(set_author_id))  # == 252726

df_main = df_main[df_main['author_id_1'].isin(set_author_id)]
df_main = df_main[df_main['author_id_2'].isin(set_author_id)]

print(df_main.shape)  # (1410374, 5)

df_main.drop(['year', 'label', 'article_id'], axis=1, inplace=True)
df_main['value'] = 1

group_df = df_main.groupby(by=['author_id_1', 'author_id_2']).sum()
print(group_df.shape)  # (903139, 1)

group_df.to_csv(PATH_TO_SAVE_DF_AUTHORS_LABELS)
