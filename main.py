from flask import Flask
from flask_cors import CORS
from config.config import db, jwt, Config, mail, migrate
from models.user_model import *
from models.child_model import *
from models.screening_model import *
from models.recomendation_model import *
from models.psychologist_model import *
from models.activity_model import *
from models.auth_model import *
from models.booking_model import *

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)
mail.init_app(app)
jwt.init_app(app)
migrate.init_app(app, db)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)