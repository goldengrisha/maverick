import re
import pickle

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


nltk.download("english")
nltk.download('stopwords')
nltk.download('wordnet')


def get_clean_text(text: str) -> str:
    lemmatizer = WordNetLemmatizer()
    cleaned_text = re.sub("[^a-zA-Z]", " ", text)
    cleaned_text = cleaned_text.lower()
    cleaned_text = cleaned_text.split()
    cleaned_text = [
        word for word in cleaned_text if word not in stopwords.words("english")
    ]
    cleaned_text = [lemmatizer.lemmatize(word) for word in cleaned_text]
    cleaned_text = " ".join(cleaned_text)

    return cleaned_text


def convert_text_to_vector(text: str) -> list:
    vectorizer = pickle.load(open("./models/vectorizer.pickle", "rb"))
    text_as_vector = vectorizer.fit_transform([text]).toarray()

    return text_as_vector
