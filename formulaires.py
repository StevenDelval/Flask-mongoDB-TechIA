from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField

class Connexion(FlaskForm):
    login = StringField("Nom utilisateur :")
    password = PasswordField("Mot de passe :")
