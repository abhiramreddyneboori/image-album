import os

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello!"


if _name_ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
