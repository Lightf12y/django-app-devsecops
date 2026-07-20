import os
import socket

import requests
from flask import Flask, jsonify

app = Flask(__name__)

INSTANCE_NAME = os.environ.get("INSTANCE_NAME", "unknown")
PEER_SERVICE = os.environ.get("PEER_SERVICE", "")


@app.route("/")
def home():
    return jsonify({
        "message": f"Salut depuis {INSTANCE_NAME} !",
        "hostname": socket.gethostname(),
    })


@app.route("/ping")
def ping():
    if not PEER_SERVICE:
        return jsonify({"error": "PEER_SERVICE non défini"}), 500

    try:
        resp = requests.get(f"http://{PEER_SERVICE}:5000/", timeout=3)
        return jsonify({
            "from": INSTANCE_NAME,
            "reached": PEER_SERVICE,
            "peer_response": resp.json(),
        })
    except requests.exceptions.RequestException as e:
        return jsonify({
            "from": INSTANCE_NAME,
            "reached": PEER_SERVICE,
            "error": str(e),
        }), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)