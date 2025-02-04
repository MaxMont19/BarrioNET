from app import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='usuario')

class Fundo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    lotes = db.relationship('Lote', backref='fundo_rel', lazy=True)

class Cultivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    lotes = db.relationship('Lote', backref='cultivo_rel', lazy=True)
    dias = db.relationship('Dias', backref='cultivo', lazy=True)

class Lote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cultivo_id = db.Column(db.Integer, db.ForeignKey('cultivo.id'), nullable=False)
    fundo_id = db.Column(db.Integer, db.ForeignKey('fundo.id'), nullable=False)  
    fecha_poda = db.Column(db.Date, nullable=False)
    tareas = db.relationship('Tarea', backref='lote', lazy=True)  # 🔥 Se maneja a nivel de tareas

class Dias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_cultivo = db.Column(db.Integer, db.ForeignKey('cultivo.id'), nullable=False)
    dias = db.Column(db.Integer, nullable=False)
    quimicos = db.relationship('Quimico', backref='dias_rel', lazy=True)

class Quimico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_comercial = db.Column(db.String(100), nullable=False)
    denominacion_ing_activo = db.Column(db.String(100), nullable=False)
    objetivo = db.Column(db.String(100), nullable=False)
    dosis_cilindro = db.Column(db.Float, nullable=False)
    dosis_hectarea = db.Column(db.Float, nullable=False)
    volumen = db.Column(db.Float, nullable=False)
    id_dias = db.Column(db.Integer, db.ForeignKey('dias.id'), nullable=False)
    tareas = db.relationship('Tarea', backref='quimico_rel', lazy=True)
    fenologia = db.Column(db.String(50), nullable=False)  

class Tarea(db.Model):
    __tablename__ = 'tarea'
    id = db.Column(db.Integer, primary_key=True)
    id_lote = db.Column(db.Integer, db.ForeignKey('lote.id'), nullable=False)
    id_quimico = db.Column(db.Integer, db.ForeignKey('quimico.id'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha_programada = db.Column(db.Date, nullable=False)
    id_dias = db.Column(db.Integer, db.ForeignKey('dias.id'), nullable=False)
    estado = db.Column(db.String(20), default="pendiente")  # 🔥 Ahora el estado está a nivel de tareas
    fecha_realizada = db.Column(db.Date, nullable=True)
    historial = db.relationship('Historial', backref='tarea', lazy=True)
    usuario_rel = db.relationship('Usuario', backref='tareas')

class Historial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_lote = db.Column(db.Integer, db.ForeignKey('lote.id'), nullable=False)
    id_tarea = db.Column(db.Integer, db.ForeignKey('tarea.id'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_quimico = db.Column(db.Integer, db.ForeignKey('quimico.id'), nullable=False)
    observacion = db.Column(db.Text, nullable=True)


