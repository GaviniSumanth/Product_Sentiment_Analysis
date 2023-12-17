from flask import Flask, render_template, request
import model

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    url = request.form["url"]
    top_review = ""
    if url:
        try:
            predicted_result, top_review = model.predict(url)
        except Exception as e:
            print(f"Error:{e}")
            predicted_result = "Reviews not found"
        return render_template(
            "predict.html", result=predicted_result, top_review=top_review
        )
    else:
        return render_template(
            "predict.html", result="URL can't be empty", top_review=top_review
        )


if __name__ == "__main__":
    app.run()
