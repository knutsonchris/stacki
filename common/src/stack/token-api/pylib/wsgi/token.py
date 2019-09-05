from flask import Flask, jsonify, request


app = Flask(__name__)

@app.route("/", methods=["POST"])
def token():
    return jsonify({"token": "TODO"}), 200
