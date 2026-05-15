from flask import Flask
from flask_cors import CORS
from config.config import db, jwt, Config, mail, migrate
from routes.routes import api_auth_bp
from models.__init__ import *

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)
mail.init_app(app)
jwt.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(api_auth_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)