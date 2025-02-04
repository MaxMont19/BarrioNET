from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import Usuario
from app.forms import RegistroForm, LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))  # Cambiado a dashboard

    form = RegistroForm()
    if form.validate_on_submit():
        existing_user = Usuario.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Ese nombre de usuario ya está en uso. Intenta con otro.', 'danger')
            return redirect(url_for('auth.register'))  # Redirigir al mismo formulario
        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        usuario = Usuario(username=form.username.data, password=hashed_password)
        db.session.add(usuario)
        db.session.commit()
        flash('Tu cuenta ha sido creada. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))  # Redirigir a la página principal después del login

    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(username=form.username.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password, form.password.data):
            login_user(usuario)

            next_page = request.args.get('next')  # Obtener la página de redirección si existe
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



