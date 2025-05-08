# app.py

from flask import Flask, jsonify, render_template
from data.items import items

app = Flask(__name__)

@app.route("/api/items")
def get_items():
    return jsonify(items)
