from flask import Flask, render_template, request
import model
import nltk
nltk.download('wordnet')
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    url = request.form["url"]
    if url:
        try:
            predicted_result = model.predict(url)
        except Exception as e:
            print(f"Error:{e}")
            predicted_result = "Reviews not found"
        return render_template("index.html", result=predicted_result)
    else:
        return render_template("index.html", result="URL can't be empty")


if __name__ == "__main__":
    app.run(debug=False)
