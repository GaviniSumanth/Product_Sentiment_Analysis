from flask_api import FlaskAPI
from flask_cors import CORS, cross_origin
from flask import request, jsonify
from model_db import Storage, Info

print("Testing Model:")
s = Storage()
URL = "https://www.flipkart.com/poco-c51-power-black-64-gb/product-reviews/itm62bcd2634619e"
print(s.get_model("product_sentiment_analysis").predict(url=URL))


def Server():
    app = FlaskAPI(__name__)
    # cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    CORS(app)

    @app.route("/result/", methods=["POST"])
    @cross_origin()
    def result():
        data = request.data
        model = Storage().get_model(data.pop("form"))
        pred = model.predict(url=URL)
        return jsonify({"result": pred})

    @app.route("/form", methods=["GET"])
    @cross_origin()
    def form():
        form_name = request.args["form"]
        return Info().get_fields(form_name)

    app.run()


Server()
