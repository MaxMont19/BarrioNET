from flask import Flask
from app import create_app, db  # Importa la app y la base de datos
from flask_migrate import Migrate
import os

app = create_app()
migrate = Migrate(app, db)  # 👈 Inicializa Flask-Migrate correctamente

if __name__ == "__main__":
    app.run(debug=True)

