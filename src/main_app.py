from flask import Flask
from load_balancer import load_balancer

app = Flask(__name__)


@app.route("/data", methods=["GET"])
def forward_request():
    return load_balancer()


if __name__ == "__main__":
    app.run(debug=True, port=5000)