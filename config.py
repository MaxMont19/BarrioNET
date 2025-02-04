import os

class Config:
    SECRET_KEY = "Max142521"  # Agrega esta línea
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Max142521@basededatoslote.cdeu6e4s2fpd.us-east-2.rds.amazonaws.com:5432/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


