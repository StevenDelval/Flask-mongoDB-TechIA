from tkinter.messagebox import NO
from flask import Flask, render_template, redirect, url_for, request, session

from pymongo import MongoClient

from formulaires import Connexion, Inscription, Commentaire , Validation, Article

from fonctions import crypt, date_in_str

client = MongoClient("localhost:27017")

db=client.blog
articles = db.articles
user=db.utilisateurs
comment=db.commentaires

app = Flask(__name__)
app.config['SECRET_KEY']='Secret'


@app.route("/") #différents url possibles du site
def accueil():
    try:
        utilisateur = session["user"]
    except:
        utilisateur = None
    return render_template("accueil.html" ,login = utilisateur, articles = articles.find().sort('date',-1) )
    

@app.route('/article/<titre>', methods=['GET','POST'])
def article(titre):
    article = articles.find_one({"titre" : titre})
    if article is None:
        return redirect(url_for("page404"))
    else:
        try:
            utilisateur = session["user"]
        except:
            utilisateur = None

        liste_commentaire=article["commentaires"]
        liste_commentaires_valides=[]
        for comment in liste_commentaire:
            if comment["validation"] :
                liste_commentaires_valides.append(comment)
        form = Commentaire()
        
        if form.validate_on_submit():
            if utilisateur is not None:
            
                commentaire={"utilisateur":utilisateur, "date":date_in_str(), "commentaire":form.data["commentaire"],"validation": False}
                liste_commentaire.append(commentaire)
                articles.update_one({"titre" : titre}, { "$set": {"commentaires":liste_commentaire} })
        
            else:
                return redirect(url_for("connexion"))

        return render_template("article.html", form=form, login=utilisateur, article = article, comments=liste_commentaires_valides)
    
@app.route('/ecrire_article', methods=['GET', 'POST'])
def ecrire_article():
    try:
        utilisateur = session["user"]
    except:
        utilisateur = None
    

    form = Article()
    if form.validate_on_submit():
        if utilisateur is not None:
            nouvel_article={"titre":form.data["titre"],"auteur":utilisateur,"resumer":form.data["resumer"], "texte":form.data["texte"],"date":date_in_str(),"commentaires" :[] }
            articles.insert_one(nouvel_article)
            return redirect(url_for("liste_articles"))

        else:
            return redirect(url_for("connexion"))
    return render_template("ecrire_article.html",login=utilisateur, form=form)

@app.route('/liste_articles')
def liste_articles():
    try:
        utilisateur = session["user"]
    except:
        utilisateur = None
    return render_template("liste_articles.html",login = utilisateur, articles=articles.find().sort('date',-1) )

@app.route('/connexion',methods=['GET','POST'])
def connexion():
    form = Connexion()
    try:
        utilisateur = session["user"]
    except:
        utilisateur = None
    if utilisateur is not None:
        return redirect(url_for("accueil"))
    if form.validate_on_submit():
        is_in_bd = user.find_one({"username":form.data["login"],"password":crypt(form.data["password"])})
        if is_in_bd is not None:
            session["user"] = is_in_bd["username"]
            return redirect(url_for("accueil"))
      
    return render_template("connexion.html",form = form)

@app.route('/inscription',methods=['GET','POST'])
def inscription():
    form =Inscription()
    try:
        utilisateur = session["user"]
    except:
        utilisateur = None
    if utilisateur is not None:
        return redirect(url_for("accueil"))
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

@app.route("/page404")
def page404():
    return render_template("page404.html")

@app.route("/admin/",methods=['GET','POST']) #à compléter
def admin():
    try:
        utilisateur = session["user"]
    except:
        utilisateur = None
    liste_articles=articles.find()
    form = Validation()
    
    if form.validate_on_submit():
        if utilisateur is not None:
            if form.validation is True :
                article["validation"] = True
                return redirect(url_for("page404"))
            else:
                pass

        else: 
               
            return redirect(url_for ("connexion"))

    
     
    for article in liste_articles:
        liste_commentaire = article["commentaires"]
        for commentaire in liste_commentaire:
            if not commentaire["validation"]:
                return render_template("page_admin.html",form = form , commentaire = commentaire)

    return render_template("page_admin.html",form = form )

    

 
