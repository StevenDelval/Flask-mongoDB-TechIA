from flask import Flask, render_template, redirect, url_for, request, session

from pymongo import MongoClient
from bson import ObjectId

from formulaires import Connexion, Inscription, Commentaire , Validation, Article,Modifier_article
from fonctions import crypt, date_in_str

client = MongoClient("localhost:27017")

db=client.blog
articles = db.articles
user=db.utilisateurs
comment=db.commentaires

app = Flask(__name__)
app.config['SECRET_KEY']='Secret'

#####################################
## Accueil                         ##
#####################################
@app.route("/") #différents url possibles du site
def accueil():
    try: ## Savoir si l'utilisateur est authentifier et a des droit admin
        utilisateur = session["user"]
        admin = session["admin"]
    except:
        utilisateur = None
        admin = False
        
    index = 0
    liste_articles =[]
    tous_les_articles = articles.find().sort('date',-1)## Recuperation de tous les articles
    for article in tous_les_articles: ## Cree une liste avec les 6 dernier articles
        if index < 6:
            liste_articles.append(article)
            index += 1



    return render_template("accueil.html" ,login = utilisateur, admin=admin, articles = liste_articles )
    

#####################################
## La page d'un article            ##
#####################################
@app.route('/article/<titre>', methods=['GET','POST'])
def article(titre):
    article = articles.find_one({"titre" : titre})
    if article is None: ## verifie si l'article existe
        return redirect(url_for("page404"))## Revoie la page 404
    else:
        try:
            utilisateur = session["user"]
            admin = session["admin"]
        except:
            utilisateur = None
            admin = False

        liste_commentaire=article["commentaires"]
        liste_commentaires_valides=[]
        for comment in liste_commentaire:
            if comment["validation"] : ## Cree une liste avec les commentaires validés
                liste_commentaires_valides.append(comment)
        form = Commentaire()
        
        if form.validate_on_submit():
            if utilisateur is not None:
                ## Ajout le commentaire de l'utilisateur dans la BDD
                commentaire={"utilisateur":utilisateur, "date":date_in_str(), "commentaire":form.data["commentaire"],"validation": False}
                liste_commentaire.append(commentaire)
                articles.update_one({"titre" : titre}, { "$set": {"commentaires":liste_commentaire} })
        
            else:
                return redirect(url_for("connexion"))

        return render_template("article.html", form=form, login=utilisateur,admin=admin, article = article, comments=liste_commentaires_valides)

#####################################
## Ecrire un article            ##
#####################################

@app.route('/ecrire_article', methods=['GET', 'POST'])
def ecrire_article():
    try:
        utilisateur = session["user"]
        admin = session["admin"]
    except:
        utilisateur = None
        admin = False
    if not admin:
        return redirect(url_for("page404"))

    form = Article()
    if form.validate_on_submit():
        if utilisateur is not None:
            #Ajout de l'article a la BDD
            nouvel_article={"titre":form.data["titre"],"auteur":utilisateur,"resumer":form.data["resumer"], "texte":form.data["texte"],"date":date_in_str(),"commentaires" :[] }
            articles.insert_one(nouvel_article)
            return redirect(url_for("liste_articles"))

        else:
            return redirect(url_for("connexion"))
    return render_template("ecrire_article.html",login=utilisateur,admin=admin, form=form)


#####################################
## Liste de tous les articles      ##
#####################################
@app.route('/liste_articles')
def liste_articles():
    try:
        utilisateur = session["user"]
        admin = session["admin"]
    except:
        utilisateur = None
        admin = False
    return render_template("liste_articles.html",login = utilisateur,admin=admin, articles=articles.find().sort('date',-1) )


#####################################
## Connexion                      ##
#####################################
@app.route('/connexion',methods=['GET','POST'])
def connexion():
    form = Connexion()
    try:
        utilisateur = session["user"]
    except:
        utilisateur = None

    if utilisateur is not None:
        return redirect(url_for("accueil"))
    erreur = None
    if form.validate_on_submit():
        is_in_bd = user.find_one({"username":form.data["login"],"password":crypt(form.data["password"])})
        if is_in_bd is not None:
            session["user"] = is_in_bd["username"]
            session["admin"] = is_in_bd["droit_admin"]
            return redirect(url_for("accueil"))
        else:
            erreur = "Utilisateur ou mot de passe non existant"
    return render_template("connexion.html",form = form, error=erreur)



#####################################
## Inscription                     ##
#####################################
@app.route('/inscription',methods=['GET','POST'])
def inscription():
    form =Inscription()
    try:
        utilisateur = session["user"]
    except:
        utilisateur = None

    if utilisateur is not None:
        return redirect(url_for("accueil"))
    erreur = None
    if form.validate_on_submit():
        is_in_bd = user.find_one({"username":form.data["login"]})
        if is_in_bd is None:
            if form.data["password"] == form.data["confirmation_password"]:
                user.insert_one({"username":form.data["login"],
                                "password":crypt(form.data["password"]),
                                "droit_admin":False,
                }
                )
                session["user"] = form.data["login"]
                session["admin"] = False
                return redirect(url_for("accueil"))
            else:
                erreur = "Mots de passe différents"
        else:
            erreur = "Utilisateur déjà pris"
    return render_template("inscription.html",form = form, error=erreur)


#####################################
## Deconnexion                     ##
#####################################
@app.route("/logout")
def logout():
    session.pop('user')
    session.pop("admin")
    return redirect(url_for("accueil"))


#####################################
## Page 404                        ##
#####################################
@app.route("/page404")
def page404():
    return render_template("page404.html")


#####################################
## Page admin                      ##
#####################################
@app.route("/admin/",methods=['GET','POST']) #à compléter
def admin():
    try:
        utilisateur = session["user"]
        admin = session["admin"]
    except:
        utilisateur = None
        admin = False
    if admin:
        liste_articles=articles.find()
        liste_des_comm_a_valider=[]
    
        for article in liste_articles:
            liste_commentaires = article["commentaires"]
            for index in range(len(liste_commentaires)):
                if not liste_commentaires[index]["validation"]:
                    ## Ajout le commentaire qui n'est pas validé a liste avec l'id de l'article,son auteur et son index dans la liste des commentaires de son article. 
                    liste_des_comm_a_valider.append([article["_id"],liste_commentaires[index]["utilisateur"],liste_commentaires[index]["commentaire"],index])
                  
        if len(liste_des_comm_a_valider) == 0 :
            liste_des_comm_a_valider=None
        
        return render_template("page_admin.html",login=utilisateur,admin=admin,commentaires=liste_des_comm_a_valider )
                

        
    else:
        return redirect(url_for("accueil"))          


#####################################
## Validation commentaire          ##
#####################################
@app.route("/admin/valider/<id_article>/<nb_comm>",methods=['GET','POST']) 
def valider_com(id_article,nb_comm):
    id_article=ObjectId(id_article)
    nb_comm=int(nb_comm)
    try:
        utilisateur = session["user"]
        admin = session["admin"]
    except:
        utilisateur = None
        admin = False
    if admin:
        article =articles.find_one({"_id":id_article})
        if article is None:
            return redirect(url_for("page404"))
    
        
        liste_commentaire=article["commentaires"]
        if nb_comm >= len(liste_commentaire):
            return redirect(url_for("admin"))
        commentaire_a_valider = liste_commentaire[nb_comm]

        form = Validation()
        if  commentaire_a_valider["validation"]:
            return redirect(url_for("admin"))
        
        if form.validate_on_submit():

            if utilisateur is not None:
                if bool(int(form.data["validation"])) :
                    liste_commentaire.pop(nb_comm)
                    commentaire_a_valider["validation"] = True
                    liste_commentaire.insert(nb_comm,commentaire_a_valider)
                    articles.update_one({"_id": id_article}, { "$set": {"commentaires":liste_commentaire} })
                    return redirect(url_for("admin"))
                else:
                    liste_commentaire.pop(nb_comm)
                    articles.update_one({"_id": id_article}, { "$set": {"commentaires":liste_commentaire} }) 
                    return redirect(url_for("admin"))

        return render_template("page_validation_com.html",login=utilisateur,admin=admin,form=form,article = article,commentaire = commentaire_a_valider)
    
#####################################
## Supprimer un article            ##
#####################################
@app.route('/article/supprimer_article/<id_article>')
def supprimer_article(id_article):
    try:
        utilisateur = session["user"]
        admin = session["admin"]
    except:
        utilisateur = None
        admin = False
    if admin:
        id_article=ObjectId(id_article)
        articles.delete_one({"_id": id_article})
        return redirect (url_for("liste_articles"))
    else:
        return redirect(url_for("accueil"))
#####################################
## Modifier un article             ##
#####################################
@app.route('/article/modifier_article/<id_article>',methods=['GET','POST'])
def modifier_article(id_article):
    try:
        utilisateur = session["user"]
        admin = session["admin"]
    except:
        utilisateur = None
        admin = False
    if admin:
        id_article=ObjectId(id_article)
        article=articles.find_one({"_id": id_article})
        form = Modifier_article()
        if form.validate_on_submit():
            if utilisateur is not None:
                articles.update_one({"_id": id_article}, { "$set": {"titre":form.data["titre"],"texte":form.data["texte"],"resumer":form.data["resumer"],"modifier":date_in_str()} })
                return redirect(url_for("article",titre=article["titre"]))

        return render_template("modification_article.html",article=article,form=form,login=utilisateur,admin=admin)
    else:
        return redirect(url_for("accueil"))