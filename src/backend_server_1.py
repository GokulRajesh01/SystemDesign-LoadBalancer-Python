from flask import Flask

app = Flask(__name__)

@app.route("/data")
def get_data():
    return "Hello from Server 1!", 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)