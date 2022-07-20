from re import U
from flask import Flask, render_template, redirect, url_for, request, session

from pymongo import MongoClient
from datetime import datetime

from formulaires import Connexion, Inscription


client = MongoClient("localhost:27017")

db=client.blog
articles = db.articles
utilisateur=db.utilisateur

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
    utilisateur = {"username":"steven","password":"1234"}
    form = Connexion()
    if form.validate_on_submit():
        if form.data["login"] == utilisateur["username"] and form.data["password"] == utilisateur["password"]:
            session["user"] = form.data["login"]
            return redirect(url_for("accueil"))
      
    return render_template("connexion.html",form = form)

@app.route('/inscription',methods=['GET','POST'])
def inscription():
    form =Inscription()
    if form.validate_on_submit():
        return redirect( "accueil")
    return render_template("inscription.html",form = form)
@app.route("/logout")
def logout():
    session.pop('user')
    return redirect(url_for("accueil"))

@app.route("/admin/") #à compléter
def admin():
    pass 