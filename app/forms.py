from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError, Regexp
from app.models import Usuario

class RegistroForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=100)])
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=4, max=50), Regexp('^[a-zA-Z0-9_]+$', message="El usuario solo puede contener letras, números y guiones bajos.")])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email(), Length(max=255)])
    distrito = StringField('Distrito', validators=[Length(max=100)])
    foto_perfil = FileField('Foto de Perfil')  # ✅ Esto solo define el campo, no lo renderiza en HTML
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6, message="Lacontraseña debe tener al menos 6 caracteres.")])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password', message="Las contraseñas deben coincidir.")])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Ese nombre de usuario ya está en uso. Elige otro.')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Ese correo electrónico ya está en uso.')

class LoginForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')
