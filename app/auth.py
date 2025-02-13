from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import Usuario
from app.forms import RegistroForm, LoginForm
import os
from werkzeug.utils import secure_filename

auth_bp = Blueprint('auth', __name__)

# Extensiones permitidas para imágenes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """ Verifica si el archivo tiene una extensión permitida. """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistroForm()
    
    if form.validate_on_submit():
        # Obtener la ruta de la carpeta `uploads` dentro del contexto de la app
        UPLOAD_FOLDER = os.path.join(current_app.root_path, 'static', 'uploads')

        # Verificar si la carpeta de subida existe, si no, crearla
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Manejo del archivo de imagen
        foto_perfil = request.files['foto_perfil']
        filename = None  # Valor por defecto si no sube imagen

        if foto_perfil and allowed_file(foto_perfil.filename):
            filename = secure_filename(foto_perfil.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            foto_perfil.save(filepath)  # Guardar la imagen en la carpeta

        # Guardar usuario en la BD
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        usuario = Usuario(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            username=form.username.data,
            email=form.email.data,
            distrito=form.distrito.data,
            foto_perfil=filename,  # Guarda solo el nombre del archivo en la BD
            password=hashed_password
        )
        db.session.add(usuario)
        db.session.commit()
        
        flash('Tu cuenta ha sido creada. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))  # ✅ Redirige a /home si ya está autenticado

    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()  # ✅ Buscar usuario por email

        if usuario and bcrypt.check_password_hash(usuario.password, form.password.data):
            login_user(usuario)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home.home'))  # ✅ Redirige a /home

        else:
            flash('Email o contraseña incorrectos', 'danger')  # ✅ Mensaje de error actualizado

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('auth.login'))

