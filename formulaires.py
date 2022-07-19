from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField

class Connexion(FlaskForm):
    login = StringField("Nom utilisateur :", render_kw={"placeholder": "Nom utilisateur "})
    password = PasswordField("Mot de passe :",render_kw={"placeholder": "Mot de passe"})
