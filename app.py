from flask import Flask, render_template, redirect, url_for, request, session

from pymongo import MongoClient
from datetime import datetime

from formulaires import Connexion, Inscription, Commentaire 


client = MongoClient("localhost:27017")

db=client.blog
articles = db.articles

app = Flask(__name__)
app.config['SECRET_KEY']='Secret'


@app.route("/") #différents url possibles du site
def accueil():
    return render_template("accueil.html" , articles = articles.find().sort('date',-1), login=session['login'] )

@app.route('/article/<titre>')
def article(titre):
    form = Commentaire()
    if form.validate_on_submit():
        if Connexion == "connecté": #à changer
            if login == blog_db[0], if password == database[1]:
                user = Connexion.login 
                date = date_in_str()
                validation = False
            else:
                return redirect(url_for("inscription"))
        else:
            return redirect(url_for("connexion"))
    return render_template("article.html", titre=titre, article = articles.find_one({"titre" : titre}))



@app.route('/liste_articles/')
def liste_articles():
    return render_template("liste_articles.html", articles=articles.find())

@app.route('/connexion',methods=['GET','POST'])
def connexion():
    form = Connexion()
    if form.validate_on_submit():
        return "connecté"
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    utilisateur = {"login": "adresse@mail.com", "password": "mdp"}
    form = Connexion()
    if form.validate_on_submit(): #pour vérifier que l'utilisateur a bien rentré des données
        if form.data["login"] == utilisateur["login"] and form.data["password"] == utilisateur["password"]: #if find_one est-ce qu'il y a qqc dans la bdd qui correspond aux logins
            #création d'une session
            session["login"] = utilisateur["login"]
            return redirect(url_for("accueil")) #renvoyer l'user vers l'accueil après connexion 
    return render_template("login.html", form=form)