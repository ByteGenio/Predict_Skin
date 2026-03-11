from flask import Flask, render_template, request
import os
import sqlite3
from predict import predict_image
from database import create_table

# create database table
create_table()

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    file = request.files["file"]

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

    file.save(filepath)

    # AI prediction
    disease, confidence, risk, recommendation = predict_image(filepath)

    # save prediction to database
    conn = sqlite3.connect("skin_disease.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO predictions(image,disease,confidence) VALUES(?,?,?)",
        (filepath, disease, confidence)
    )

    conn.commit()
    conn.close()

    return render_template(
        "result.html",
        disease=disease,
        confidence=round(confidence, 2),
        risk=risk,
        recommendation=recommendation,
        img_path=filepath
    )


# prediction history page
@app.route("/history")
def history():

    conn = sqlite3.connect("skin_disease.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions")

    data = cursor.fetchall()

    conn.close()

    return render_template("history.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)