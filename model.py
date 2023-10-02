import pickle
from numpy import bincount, array, argmax
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from nltk import WordNetLemmatizer
import nltk

nltk.download("wordnet")

with open("models/classifier.model", "rb") as f:
    model = pickle.loads(f.read())

with open("models/vector.model", "rb") as f:
    vectorizer = pickle.loads(f.read())

with open("models/stopwords.model", "rb") as f:
    stopwords = pickle.loads(f.read())


def clean(text):
    lemmatizer = WordNetLemmatizer()
    text = str(text).encode("ascii", "ignore").decode("ascii")
    text = str(text).lower()
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"'s", " ", text)
    text = re.sub(r"'ve", " have ", text)
    text = re.sub(r"can't", "can not ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"'re", " are ", text)
    text = re.sub(r"'d", " would ", text)
    text = re.sub(r"'ll", " will ", text)
    text = [word for word in text.split(" ") if word not in stopwords]
    text = " ".join(text)
    text = [lemmatizer.lemmatize(word) for word in text.split(" ")]
    text = " ".join(text)
    return text


def predict(url):
    review_url = url.replace("/p/", "/product-reviews/")
    pages = 3
    reviews_list = []
    for p in range(1, pages + 1):
        url = review_url + f"?sortOrder=MOST_HELPFUL&page={p}"
        webpage = requests.get(url)
        soup = BeautifulSoup(webpage.content, "html.parser")
        reviews_html = soup.find("div", {"class": "_1YokD2 _3Mn1Gg col-9-12"}).find_all(
            "div", {"class": "_1AtVbE col-12-12"}
        )
        for id in range(len(reviews_html)):
            if id > 1 and id < 12:
                try:
                    review = reviews_html[id].find("div", {"class": ""}).div.text
                    reviews_list.append(review)
                except Exception as e:
                    print(f"Error:{e}")
    df = pd.DataFrame({"review": reviews_list})
    df["review"] = df["review"].apply(clean)
    reviews_corpus = vectorizer.transform(df.review)
    pred = model.predict(reviews_corpus)
    counts = bincount((array(pred)))
    match argmax(counts):
        case 0:
            x = "This product is not worth buying."
        case 1:
            x = "This product seems to be ok."
        case 2:
            x = "The product is worth buying."
    return x
