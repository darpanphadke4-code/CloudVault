from flask import Flask
from flask_bcrypt import Bcrypt

from config import Config
from models import db

from routes.main import main
from routes.auth import auth
from routes.dashboard import dashboard
from routes.files import files


app = Flask(__name__)

# Configuration
app.config.from_object(Config)

# Extensions
db.init_app(app)
bcrypt = Bcrypt(app)

# Make bcrypt accessible inside blueprints
app.bcrypt = bcrypt

# Register Blueprints
app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(files)


# Run locally
if __name__ == "__main__":

    # Create database tables only for local development
    with app.app_context():
        db.create_all()

    app.run(debug=True)