from crypt import methods
from flask import Flask, render_template, redirect, url_for, request, session
from pymongo import MongoClient
from datetime import datetime
from formulaires import Connexion

""" now = datetime.now()
date_format_str = "%d/%m/%Y %H:%M:%S.%f"
date_now = now.strftime(date_format_str) """

client = MongoClient("localhost:27017")

db=client.blog
articles = db.articles

app = Flask(__name__)
app.config['SECRET_KEY']='Secret'


@app.route("/") #différents url possibles du site
def accueil():
    return render_template("accueil.html")

@app.route('/article/<nom>')
def article(nom):
    return render_template("article.html", titre=nom)

@app.route('/liste_articles/')
def liste_articles():
    return render_template("liste_articles.html", articles=articles.find())

@app.route('/connexion',methods=['GET','POST'])
def connexion():
    form = Connexion()
    return render_template("connexion.html",form = form)
@app.route('/inscription')
def inscription():
    return render_template("inscription.html")
    
@app.route("/admin/") #à compléter
def admin():
    pass
    return render_template("article.html") 