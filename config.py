import os

class Config:
    SECRET_KEY = "Max14252"  # Agrega esta línea
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Max14252@localhost:5432/BarrioNet"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}



