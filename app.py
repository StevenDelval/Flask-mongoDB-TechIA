import hashlib
from flask import Flask, render_template, redirect, url_for, request, session

from pymongo import MongoClient
from datetime import datetime

from formulaires import Connexion, Inscription

def crypt(password):
    """
    Fonction qui crypte un mot de passe
    :param password: (str) mot de passe
    :return: (str) le hash du mot de passe
    """
    hash_pwd = hashlib.new('sha256')
    hash_pwd.update(password.encode())
    hash_pwd = hash_pwd.hexdigest()
    return hash_pwd

client = MongoClient("localhost:27017")

db=client.blog
articles = db.articles
user=db.utilisateur

app = Flask(__name__)
app.config['SECRET_KEY']='Secret'


@app.route("/") #différents url possibles du site
def accueil():
    try:
        utilisateur = session["user"]
    except:
        utilisateur = None
    return render_template("accueil.html" ,login = utilisateur, articles = articles.find().sort('date',-1) )

@app.route('/article/<titre>')
def article(titre):
    try:
        utilisateur = session["user"]
    except:
        utilisateur = None
    return render_template("article.html",login = utilisateur, titre=titre, article = articles.find_one({"titre" : titre}))

@app.route('/liste_articles/')
def liste_articles():
    try:
        utilisateur = session["user"]
    except:
        utilisateur = None
    return render_template("liste_articles.html",login = utilisateur, articles=articles.find())

@app.route('/connexion',methods=['GET','POST'])
def connexion():
    form = Connexion()
    if form.validate_on_submit():
        is_in_bd = user.find_one({"username":form.data["login"],"password":crypt(form.data["password"])})
        if is_in_bd is not None:
            session["user"] = is_in_bd["username"]
            return redirect(url_for("accueil"))
      
    return render_template("connexion.html",form = form)

@app.route('/inscription',methods=['GET','POST'])
def inscription():
    form =Inscription()
    if form.validate_on_submit():
        is_in_bd = user.find_one({"username":form.data["login"]})
        if is_in_bd is None:
            if form.data["password"] == form.data["confirmation_password"]:
                user.insert_one({"username":form.data["login"],
                                "password":crypt(form.data["password"])
                }
                )
                session["user"] = form.data["login"]
                return redirect(url_for("accueil"))
        return redirect( url_for("inscription"))
    return render_template("inscription.html",form = form)
@app.route("/logout")
def logout():
    session.pop('user')
    return redirect(url_for("accueil"))

@app.route("/admin/") #à compléter
def admin():
    pass 