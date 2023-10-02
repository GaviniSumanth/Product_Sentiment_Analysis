from flask import Flask, render_template, request
import model

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", result="")


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


app.run(host="0.0.0.0", port=5000, debug=True)
