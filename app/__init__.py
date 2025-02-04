from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# Inicialización de extensiones
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

# Configuración de Flask-Login
login_manager.login_view = 'auth.login'  
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.auth import auth_bp
    from app.routes import main_bp  # ❌ Eliminado calcular_fechas_programadas

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp, url_prefix="/")

    return app

# Cargar usuario para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from app.models import Usuario  # Evitar errores circulares
    return Usuario.query.get(int(user_id))






