import requests
import pandas as pd
from bs4 import BeautifulSoup


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
            review = box.select_one('[data-hook="review-body"]').text.strip()
        except Exception as e:
            review = "N/A"
        data_dict = {
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


page_url = "https://www.amazon.com/dp/B0CBP49GLZ/ref=sspa_dk_detail_2?psc=1&pd_rd_i=B0CBP49GLZ&content-id=amzn1.sym.0d1092dc-81bb-493f-8769-d5c802257e94&s=electronics&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWwy"
print(getReviews(page_url))
