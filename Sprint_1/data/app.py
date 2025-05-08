# app.py

from flask import Flask, jsonify, render_template
from data.items import items

app = Flask(__name__)

@app.route("/api/items")
def get_items():
    return jsonify(items)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/wardrobe")
def wardrobe():
    return render_template("wardrobe.html", items=items)

if __name__ == "__main__":
    app.run(debug=True)
