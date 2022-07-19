from flask import Flask, render_template, redirect, url_for, request, session

from pymongo import MongoClient
from datetime import datetime

from formulaires import Connexion, Inscription


client = MongoClient("localhost:27017")

db=client.blog
articles = db.articles

app = Flask(__name__)
app.config['SECRET_KEY']='Secret'


@app.route("/") #différents url possibles du site
def accueil():
    return render_template("accueil.html" , articles = articles.find().sort('date',-1) )

@app.route('/article/<titre>')
def article(titre):
    return render_template("article.html", titre=titre, article = articles.find_one({"titre" : titre}))

@app.route('/liste_articles/')
def liste_articles():
    return render_template("liste_articles.html", articles=articles.find())

@app.route('/connexion',methods=['GET','POST'])
def connexion():
    form = Connexion()
    if form.validate_on_submit():
        return "connecter"
    return render_template("connexion.html",form = form)

@app.route('/inscription',methods=['GET','POST'])
def inscription():
    form =Inscription()
    if form.validate_on_submit():
        return redirect( url_for("accueil"))
    return render_template("inscription.html",form = form)
    
@app.route("/admin/") #à compléter
def admin():
    pass 