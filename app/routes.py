from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    return redirect(url_for('auth.login'))  # 🔄 Mantiene la redirección inicial al login

@home_bp.route('/home')
@login_required
def home():
    return render_template('home.html', usuario=current_user)  # 🔹 Renderiza home.html
