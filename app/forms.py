from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models import Usuario
from app.models import Fundo, Cultivo

class RegistroForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Ese nombre de usuario ya está en uso. Elige otro.')

class LoginForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class LoteForm(FlaskForm):
    nombre = StringField('Nombre del Lote', validators=[DataRequired()])
    fundo = SelectField('Fundo', coerce=int, validators=[DataRequired()])
    cultivo = SelectField('Cultivo', coerce=int, validators=[DataRequired()])
    fecha_poda = DateField('Fecha de Poda', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        super(LoteForm, self).__init__(*args, **kwargs)
        self.fundo.choices = [(f.id, f.nombre) for f in Fundo.query.all()]
        self.cultivo.choices = [(c.id, c.nombre) for c in Cultivo.query.all()]