"""transform df['description']"""

import contractions
import nltk
import re
from nltk.corpus import stopwords

# nltk.download('punkt')
# nltk.download('stopwords')


def remove_noise(text):
    text = re.sub(r",", "", text)
    text = re.sub(r"\w+\d+", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"\$", "dollar ", text)
    text = re.sub(r"\$+", "dollar ", text)
    text = re.sub(r"dollars", "dollar", text)
    text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
    text = re.sub(r"!", " ", text)
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r":", "", text)
    text = re.sub(r" :", "", text)
    text = re.sub(r"\w+\-\w+", "", text)
    text = re.sub(r" -", "", text)
    text = re.sub(r" s ", "", text)
    text = re.sub(r" - ", "", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    # text = re.sub(r",", "", text)
    # text = re.sub(r"\.", " ", text)
    text = re.sub(r"!", " ! ", text)
    text = re.sub(r"\/", " ", text)
    text = re.sub(r"\^", " ^ ", text)
    text = re.sub(r"\+", " + ", text)
    text = re.sub(r"\-", " - ", text)
    text = re.sub(r"\=", " = ", text)
    text = re.sub(r"'", " ", text)
    text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
    text = re.sub(r":", " : ", text)
    text = re.sub(r" e g ", " eg ", text)
    text = re.sub(r" b g ", " bg ", text)
    text = re.sub(r" u s ", " american ", text)
    text = re.sub(r"\0s", "0", text)
    text = re.sub(r" 9 11 ", "911", text)
    text = re.sub(r"e - mail", "email", text)
    text = re.sub(r"j k", "jk", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"", "", text)
    return text


def remove_noise2(text):
    text = text.replace(".", "")
    return text


def expand_contractions(text):
    return contractions.fix(text)


def remove_stopwords3(text):
    # remove stopwords
    stop_words = stopwords.words("english")

    tokens = nltk.word_tokenize(text)
    filtered_words = [w for w in tokens if len(w) > 2 if w not in stop_words]

    return " ".join(filtered_words)


def clean_text(df):
    df["description"] = df["title"] + df["abstract"]
    df["description"] = (
        df.description.map(lambda description: description.lower())
        .map(remove_noise)
        .map(expand_contractions)
        .map(remove_noise2)
        .map(remove_stopwords3)
    )

    return df
