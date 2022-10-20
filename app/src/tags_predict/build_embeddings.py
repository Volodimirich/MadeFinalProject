import sister


bert_embedding = sister.MeanEmbedding(lang="en")


def build_embed(df):
    embed = list(map(bert_embedding, df.description))
    return embed
