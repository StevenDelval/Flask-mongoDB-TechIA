from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField

class Connexion(FlaskForm):
    login = StringField("Nom utilisateur :", render_kw={"placeholder": "Nom utilisateur "})
    password = PasswordField("Mot de passe :",render_kw={"placeholder": "Mot de passe"})

class Inscription(FlaskForm):
    login = StringField("Nom utilisateur :", render_kw={"placeholder": "Nom utilisateur "})
    password = PasswordField("Mot de passe :",render_kw={"placeholder": "Mot de passe"})
    confirmation_password = PasswordField("Confirmation mot de passe :",render_kw={"placeholder": "Confirmation mot de passe"})

class Commentaire(FlaskForm):
    commentaire = StringField("Commentaire : ", render_kw={"placeholder": "Entrez votre commentaire"})
  