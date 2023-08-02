from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import requests
import json


class ProductInfo:
    """
    It is a class used to store the product info fetched from Flipkart.\n
    """

    class Review:
        """
        It is a class used to store a review. It has the following attributes:\n
        rating - Stores the rating (Max rating is 5)\n
        title - Stores the title of the review in string format\n
        review - Stores the content of the review
        """

        def __init__(self, rating: int, review_title: str, review: str) -> None:
            self.rating: int = rating or 0
            self.review_title: str = review_title or ""
            self.review: str = review or ""

    def __init__(self) -> None:
        self.name: str = ""
        self.product_url: str = ""
        self.query_url: str = ""
        self.reviews: list[ProductInfo.Review] = []

    def set_name(self, name: str) -> None:
        """
        Sets the name of the product
        """
        self.name = name

    def set_query_url(self, query_url: str) -> None:
        """
        Sets the query_url (URL used for fetching product info) attribute of the product
        """
        self.query_url = query_url

    def set_product_url(self, product_url: str) -> None:
        """
        Sets the product_url (URL of the product's page) attribute of the product
        """
        self.product_url = product_url

    def add_review(self, rating: int, review_title: str, review: str) -> None:
        """
        Adds a review in the form of a ProductInfo.Review object to reviews attribute
        """
        self.reviews.append(ProductInfo.Review(rating, review_title, review))

    def get_review_url(self) -> str:
        """
        Returns the reviews URL (URL of the product's reviews page)
        """
        return self.product_url.replace("/p/", "/product-reviews/")

    def to_df(self) -> pd.DataFrame:
        """
        Converts the ProductInfo Object to a Pandas DataFrame.\n
        Each row in the DataFrame contains:
        - name
        - product_url
        - query_url
        - review_url
        - rating
        - review_title
        - review
        """
        return pd.DataFrame(
            [
                {
                    "name": self.name,
                    "product_url": self.product_url,
                    "query_url": self.query_url,
                    "review_url": self.get_review_url(),
                    "rating": self.reviews[i].rating,
                    "review_title": self.reviews[i].review_title,
                    "review": self.reviews[i].review,
                }
                for i in range(self.reviews.__len__())
            ]
        )


class Flipkart:
    WEBSITE_URL: str = "https://www.flipkart.com/"
    SEARCH_API_BASEURL: str = "https://flipkart.dvishal485.workers.dev/search/"
    PRODUCT_INFO_API_BASEURL: str = "https://flipkart.dvishal485.workers.dev/product/"

    def check_connection() -> bool:
        """
        Checks if Flipkart website is reachable and prints the status code
        and returns a boolean based on the connection status.\n
            True - If website is reachable\n
            False - If website is unreachable
        """
        status = urllib.request.urlopen(Flipkart.WEBSITE_URL).getcode()
        if status >= 200 and status < 300:
            print(f"URL ({Flipkart.WEBSITE_URL}) is Working\nStatus: {status}")
            return True
        else:
            print(f"Website is down.\nStatus: {status}")
            return False

    def search(param: str = "") -> list[ProductInfo]:
        """
        A function to fetch product page URLs from flipkart based on a query parameter in string format.\n
        It returns a list of ProductInfo Objects containing:\n
            name - name of product\n
            product_url - URL of the product's page\n
            query_url - URL used for fetching product info
        """
        SEARCH = lambda x: json.loads(
            requests.get(Flipkart.SEARCH_API_BASEURL + str(x)).content
        )["result"]
        products = []
        for i in SEARCH(param):
            item = ProductInfo()
            item.set_name(i["name"])
            item.set_product_url(i["link"])
            item.set_query_url(i["query_url"])
            products.append(item)
        return products

    def get_reviews(
        products_info: list[ProductInfo],
        sort_order: str = "MOST_HELPFUL",
        pages: int = 1,
    ) -> list[ProductInfo]:
        """
        A function to fetch reviews from a product's review page.\n
        It accepts a list of ProductInfo objects which must contain a valid url in product_url attribute.\n
        Sort Order Options:\n
        - MOST_HELPFUL (default)
        - MOST_RECENT
        - POSITIVE_FIRST
        - NEGATIVE_FIRST\n
        Pages:
            The number of review pages that need to be scraped.
        It returns the objects after adding the reviews.
        """
        for i in range(len(products_info)):
            for p in range(1, pages + 1):
                url = (
                    products_info[i].get_review_url()
                    + f"?sortOrder={sort_order}&page={p}"
                )
                try:
                    webpage = requests.get(url)
                    soup = BeautifulSoup(webpage.content, "lxml")
                    reviews_html = soup.find(
                        "div", {"class": "_1YokD2 _3Mn1Gg col-9-12"}
                    ).find_all("div", {"class": "_1AtVbE col-12-12"})
                except Exception as e:
                    continue
                for id in range(len(reviews_html)):
                    if id > 1 and id < 12:
                        try:
                            review = (
                                reviews_html[id].find("div", {"class": ""}).div.text
                            )
                            title = reviews_html[id].div.div.div.div.p.text
                            rating = reviews_html[id].div.div.div.div.div.text
                            products_info[i].add_review(
                                rating=rating, review_title=title, review=review
                            )
                        except Exception as e:
                            print(f"Error:{e}")
        return products_info
