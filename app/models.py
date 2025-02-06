from app import db
from flask_login import UserMixin

# Modelo de Usuario
class Usuario(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    distrito = db.Column(db.String(100), nullable=True)
    foto_perfil = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    # Relaciones
    mensajes_enviados = db.relationship('Mensaje', foreign_keys='Mensaje.emisor_id', backref='emisor', lazy=True)
    mensajes_recibidos = db.relationship('Mensaje', foreign_keys='Mensaje.receptor_id', backref='receptor', lazy=True)
    publicaciones = db.relationship('Publicacion', backref='usuario', lazy=True)
    reportes = db.relationship('Reporte', backref='usuario', lazy=True)
    amigos = db.relationship('Amigo', 
        primaryjoin="or_(Usuario.id == Amigo.user1_id, Usuario.id == Amigo.user2_id)", 
        backref='usuario', lazy=True)
    ecopuntos = db.relationship('Ecopunto', backref='usuario', lazy=True)

# Modelo de Amigos
class Amigo(db.Model):
    __tablename__ = 'amigos'
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    status = db.Column(db.String(10), nullable=False)

# Modelo de Mensajes
class Mensaje(db.Model):
    __tablename__ = 'mensajes'
    id = db.Column(db.Integer, primary_key=True)
    emisor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receptor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

# Modelo de Reportes
class Reporte(db.Model):
    __tablename__ = 'reportes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    ubicacion = db.Column(db.Text)  # Geography data puede manejarse como text o PostGIS
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

# Modelo de Ecopuntos
class Ecopunto(db.Model):
    __tablename__ = 'ecopuntos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    puntos = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

# Modelo de Publicaciones
class Publicacion(db.Model):
    __tablename__ = 'publicaciones'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    # Relación con hashtags
    hashtags = db.relationship('PublicacionHashtag', backref='publicacion', lazy=True)

# Modelo de Hashtags
class Hashtag(db.Model):
    __tablename__ = 'hashtags'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

# Tabla intermedia entre publicaciones y hashtags
class PublicacionHashtag(db.Model):
    __tablename__ = 'publicacion_hashtag'
    publicacion_id = db.Column(db.Integer, db.ForeignKey('publicaciones.id'), primary_key=True)
    hashtag_id = db.Column(db.Integer, db.ForeignKey('hashtags.id'), primary_key=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
