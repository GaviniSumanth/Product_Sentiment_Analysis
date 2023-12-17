import pickle
from numpy import bincount, array, argmax
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from nltk import WordNetLemmatizer
import nltk

downloader = nltk.downloader.Downloader()
downloader._update_index()
downloader.download("wordnet")

with open("models/classifier.model", "rb") as f:
    model = pickle.loads(f.read())

with open("models/vector.model", "rb") as f:
    vectorizer = pickle.loads(f.read())

with open("models/stopwords.model", "rb") as f:
    stopwords = pickle.loads(f.read())


def reviewsHtml(url):
    soups = []
    for page_no in range(1, 5):
        params = {
            "ie": "UTF8",
            "reviewerType": "all_reviews",
            "filterByStar": "critical",
            "pageNumber": page_no,
        }
        response = requests.get(
            url,
            headers={
                "authority": "www.amazon.com",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-language": "en-US,en;q=0.9,bn;q=0.8",
                "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
            },
        )
        soup = BeautifulSoup(response.text, "lxml")
        soups.append(soup)
    return soups


def getPagewiseReviews(html_data):
    data_dicts = []
    boxes = html_data.select('div[data-hook="review"]')
    for box in boxes:
        try:
            stars = (
                box.select_one('[data-hook="review-star-rating"]')
                .text.strip()
                .split(" out")[0]
            )
        except Exception as e:
            stars = "N/A"
        try:
            review = box.select_one('[data-hook="review-body"]').text.strip()
        except Exception as e:
            review = "N/A"
        data_dict = {
            "stars": stars,
            "review": review,
        }
        data_dicts.append(data_dict)
    return data_dicts


def getReviews(page_url):
    reviews_url = page_url.replace("/dp/", "/product-reviews/")
    html_datas = reviewsHtml(reviews_url)
    reviews = []
    for html_data in html_datas:
        review = getPagewiseReviews(html_data)
        reviews += review
    return pd.DataFrame(reviews)


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
    df = getReviews(url)
    df["review"] = df["review"].apply(clean)
    reviews_corpus = vectorizer.transform(df.review)
    pred = model.predict(reviews_corpus)
    counts = bincount((array(pred)))
    df["stars"] = df["stars"].apply(float)
    match argmax(counts):
        case 2:
            x = 1
        case _:
            x = 0
    if len(df[df["stars"] > 4]) > len(df[df["stars"] <= 4]):
        x += 1
    else:
        x -= 1
    return (
        "This product is worth buying. You should buy it."
        if x >= 1
        else "This product is not worth buying. Do not buy it."
    )
