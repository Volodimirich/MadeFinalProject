import json
import re

try:
    import ujson
except ModuleNotFoundError:
    ujson = json
import pandas as pd
from tqdm import tqdm


regex_spec_symbol = re.compile(r'[\.\,\?\!\(\)\/\$\{\}\[\]\@\^]+')
regex_spec_symbol_to_space = re.compile(r'[\“\"\']+')
regex_multi_space_to_space = re.compile(r'\s+')


def get_text(dict_line: dict) -> str:
    title: str = dict_line.get('abstract', '')
    abstract: str = dict_line.get('title', '')

    if len(title) > 0 and len(abstract) > 0:
        if title.lower() in abstract.lower():
            return abstract
        elif abstract.lower() in title.lower():
            return title

    return title + ' ' + abstract


def preprocess_word(word: str) -> str:
    """
    Preprocess word

    :param word: word

    :return: cleaning word
    """

    word_new = regex_spec_symbol.sub('', word.lower())
    word_new = regex_spec_symbol_to_space.sub(' ', word_new)
    word_new = regex_multi_space_to_space.sub(' ', word_new)

    return word_new


SET_POPULAR_FOS = {
    'Software Engineering',
    'Political science',
    'Humanities',
    'Pattern recognition',
    'Algorithm',
    'Mathematical optimization',
    'Discrete mathematics',
    'Combinatorics',
    'World Wide Web',
    'Control theory',
    'Data science',
    'Knowledge management',
    'Neuroscience',
    'Computer vision',
    'Computer security',
    'Wireless network',
    'Computer network',
    'Mathematical optimization',
    'Applied mathematics',
    'Mathematical analysis',
    'Data mining',
    'Biology',
    'Programming language',
    'Information retrieval'
}

N_CHUNK = 50_000
PATH_RAW_DATA = '../dblpv13.jsonl'
PATH_TO_SAVE_DATAFRAME = 'all_id_for_split.csv'

with open(PATH_RAW_DATA, 'r', encoding='utf-8') as fio:
    i = 0
    data_for_df = {
        '_id': [],
        'n_word': [],
        'year': [],
        'n_keyword': [],
        'n_citation': [],
        'has_fos': [],
        'has_most_popular_fos': []
    }
    header = True

    for line in tqdm(fio):
        i += 1

        dict_line = ujson.loads(line)

        fos = set(dict_line.get('fos', []))

        text = get_text(dict_line)

        collect_word = text.split()

        text = ' '.join(map(preprocess_word, collect_word))

        data_for_df['_id'].append(dict_line['_id'])
        data_for_df['n_word'].append(len(text.split()))
        data_for_df['year'].append(dict_line.get('year'))
        data_for_df['n_keyword'].append(len(dict_line.get('keywords', [])))
        data_for_df['n_citation'].append(dict_line.get('n_citation'))
        data_for_df['has_fos'].append(bool(fos))
        data_for_df['has_most_popular_fos'].append(bool(fos & SET_POPULAR_FOS))

        if i % N_CHUNK == 0:
            df_chunk = pd.DataFrame(data_for_df)
            df_chunk.to_csv(PATH_TO_SAVE_DATAFRAME, mode='a', sep=',', header=header, index=False)

            header = False

            del df_chunk
            del data_for_df

            data_for_df = {
                '_id': [],
                'n_word': [],
                'year': [],
                'n_keyword': [],
                'n_citation': [],
                'has_fos': [],
                'has_most_popular_fos': []
            }
