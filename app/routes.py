from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Publicacion
import os
from datetime import datetime
import pytz  # Importar pytz para la zona horaria

home_bp = Blueprint('home', __name__)

# Ruta correcta para guardar imágenes en app/static/uploads
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static', 'uploads')

# Asegurar que el directorio de imágenes existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@home_bp.route('/')
def index():
    return redirect(url_for('auth.login'))  # 🔄 Mantiene la redirección inicial al login

@home_bp.route('/home')
@login_required
def home():
    publicaciones = Publicacion.query.order_by(Publicacion.created_at.desc()).all()
    return render_template('home.html', usuario=current_user, publicaciones=publicaciones)

@home_bp.route('/mapa')
@login_required
def mapa():
    return render_template('mapa.html', usuario=current_user)  # Renderiza mapa.html

@home_bp.route('/ecopuntos')
@login_required
def ecopuntos():
    return render_template('ecopuntos.html', usuario=current_user)  # Renderiza ecopuntos.html

@home_bp.route('/publicar', methods=['POST'])
@login_required
def publicar():
    contenido = request.form.get('contenido')
    imagenes = request.files.getlist('imagenes')  # Se obtiene una lista de imágenes
    hashtag = request.form.get('hashtag')
    ubicacion = request.form.get('ubicacion')

    filenames = []  # Lista para almacenar los nombres de archivo

    if imagenes:
        for imagen in imagenes:
            if imagen.filename:  # Asegurarse de que haya un archivo seleccionado
                imagen_filename = imagen.filename.replace(" ", "_")  # Evita problemas con espacios
                imagen_path = os.path.join(UPLOAD_FOLDER, imagen_filename)
                imagen.save(imagen_path)
                filenames.append(imagen_filename)  # Solo guardar el nombre del archivo

    # 📌 **Corregir la fecha con la zona horaria correcta**
    tz = pytz.timezone('America/Lima')
    fecha_actual = datetime.now(tz)

    nueva_publicacion = Publicacion(
        user_id=current_user.id,
        contenido=contenido,
        imagen=",".join(filenames),  # Guardar nombres de imágenes separados por comas
        hashtag=hashtag,
        ubicacion=ubicacion,
        created_at=fecha_actual
    )

    db.session.add(nueva_publicacion)
    db.session.commit()

    flash('Publicación creada con éxito', 'success')
    return redirect(url_for('home.home'))
