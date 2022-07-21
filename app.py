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

#####################################
## Accueil                         ##
#####################################
@app.route("/") #différents url possibles du site
def accueil():
    try:
        utilisateur = session["user"]
        admin = session["admin"]
    except:
        utilisateur = None
        admin = False
        
    index = 0
    liste_articles =[]
    tous_les_articles = articles.find().sort('date',-1)
    for article in tous_les_articles:
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
    if article is None:
        return redirect(url_for("page404"))
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
    

    form = Article()
    if form.validate_on_submit():
        if utilisateur is not None:
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
## Connecxion                      ##
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
    if form.validate_on_submit():
        is_in_bd = user.find_one({"username":form.data["login"],"password":crypt(form.data["password"])})
        if is_in_bd is not None:
            session["user"] = is_in_bd["username"]
            session["admin"] = is_in_bd["droit_admin"]
            return redirect(url_for("accueil"))
      
    return render_template("connexion.html",form = form)



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
        return redirect( url_for("inscription"))
    return render_template("inscription.html",form = form)


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
        form = Validation()
    
        for article in liste_articles:
            liste_commentaire = article["commentaires"]
            for commentaire in liste_commentaire:
                if not commentaire["validation"]:
                    REDIRECTION = render_template("page_admin.html",form = form,article=article  ,commentaire = commentaire)
                

        if form.validate_on_submit():
            if utilisateur is not None:
          
                if bool(int(form.data["validation"])) :
                    print(article["titre"],end="\n\n")
                    article_du_commentaire = articles.find_one({"titre": article["titre"] })
                    liste_commentaire_de_l_article= article_du_commentaire ["commentaires"]
                    print(liste_commentaire_de_l_article,end="\n\n")
                    liste_commentaire_de_l_article.remove(commentaire)
                    print(liste_commentaire_de_l_article)
                    commentaire["validation"] = True
                    liste_commentaire_de_l_article.append(commentaire)
                    print(liste_commentaire_de_l_article,end="\n\n")

                    articles.update_one({"titre": article["titre"] }, { "$set": {"commentaires":liste_commentaire_de_l_article} })
    else:
        return redirect(url_for("accueil"))          
                
               
                
                
    
            
            
            

   

    return REDIRECTION


@app.route("/admin/valider/<id_article>/<nb_comm>")   
def valider_com(id_article,nb_comm):
    pass
 
