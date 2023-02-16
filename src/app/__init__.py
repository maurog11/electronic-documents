from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_httpauth import HTTPTokenAuth


def create_app():

    # Inicializamos SQLAlchemy
    db.init_app(app)


# Obtiene la instancia de Flask
app = Flask(__name__)
# Token Bearer
# auth = HTTPTokenAuth(scheme='Bearer')
# CORS(app)
app.config['RESTX_MASK_SWAGGER'] = False
# Aplicamos la configuración
app.config.from_object(Config())

# SQLAlchemy
db = SQLAlchemy()
db.init_app(app)

# Flask
create_app()

# Migraciones Flask
migrate = Migrate(app, db)
