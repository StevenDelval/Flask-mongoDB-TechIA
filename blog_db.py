from pymongo import MongoClient
from datetime import datetime
import hashlib

def date_in_str():
    now = datetime.now()
    date_format_str = "%d/%m/%Y %H:%M:%S.%f"
    date_now = now.strftime(date_format_str)
    return date_now

def str_in_date(date):
    date_format_str = "%d/%m/%Y %H:%M:%S.%f"
    return  datetime.strptime(date, date_format_str)

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

client = MongoClient("127.0.0.1:27017") 

client.drop_database('blog')

db=client.blog
articles = db.articles
user=db.utilisateurs


article1 ={
    "titre" : "Simplon",
    "auteur" : "JP",
    "resumer" : "blablalbla  bla bla bla",
    "texte" : "La formation à Simplon est dure. Quam ut exagitabat satisfaceret ultimum tempestate coalito quem asperum ad inopia est saevum exagitabat quem ultimum est satisfaceret atque convectio ire ad quem asperum praetorio ad exagitabat satisfaceret coalito impedita militem et ultimum et satisfaceret trusus ultimum feritas inopia militem tempestate quam ad sit sit Rufinus asperum trusus compellebatur monstraret ipse ire quem atque ad dignitates dignitates simul causam et est convectio et et satisfaceret convectio et Rufinus more et discrimen simul impedita ordinarias impedita simul monstraret praetorio ad ea ad more ire exagitabat semper militem exagitabat ire inopia annonae causam Rufinus ipse annonae semper simul coalito semper coalito quam.",
    "date" : date_in_str(),
    "commentaires" : [{"utilisateur":"Claire", "date":date_in_str(), "commentaire":"Waaa","validation": True},{"utilisateur":"Tom", "date":date_in_str(), "commentaire":"Waaa","validation": False}]
}

article2 ={
    "titre" : "Les bananes",
    "auteur" : "Thomas",
    "resumer" : "blablalbla  bla bla bla",
    "texte" : "Les bananes sont délicieuses.",
    "date" : date_in_str(),
    "commentaires" :[]
    
}
# [{"utilisateur":"Tom", "date":date_in_str(), "commentaire":"Waaa","validation": True}]
articles.insert_many([article1, article2])

user.insert_one({
    "username" : "test",
    "password" : crypt("test")
})

