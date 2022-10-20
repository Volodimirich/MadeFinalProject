from . import transform_paper
from . import build_embeddings
import pandas as pd
from catboost import CatBoostClassifier

PATH = "./model"


def one_predict(_id: str, title: str, abstract: str):
    df = pd.DataFrame({"id": _id, "title": title, "abstract": abstract})
    _, pred = model_predict(df)
    return pred


def model_predict(df, path=PATH):
    df_clean = transform_paper.clean_text(df)
    embed = build_embeddings.build_embed(df_clean)
    df_emb = pd.DataFrame(embed, columns=[str(i) for i in range(300)])
    df_emb.set_index(df._id)

    model = CatBoostClassifier()
    model.load_model(path)

    predictions = model.predict(df_emb)

    return df._id, predictions
