from flask import Flask
from config.config import test_connection, db

app = Flask(__name__)


if __name__ == "__main__":
    test_connection()
    app.run(debug=True)