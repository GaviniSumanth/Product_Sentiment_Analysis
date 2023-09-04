from flask_api import FlaskAPI
from flask_cors import CORS, cross_origin
from flask import request, jsonify
import model


def Server():
    app = FlaskAPI(__name__)
    # cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    CORS(app)

    @app.route("/result/", methods=["POST"])
    @cross_origin()
    def result():
        data = request.data
        pred = model.get_result(data["url"])
        return jsonify({"result": pred})

    @app.route("/form", methods=["GET"])
    @cross_origin()
    def form():
        return jsonify([{"identifier": "url", "label": "Enter URL:", "type": "text"}])

    app.run()


Server()
