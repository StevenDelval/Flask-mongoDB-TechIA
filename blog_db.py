from pymongo import MongoClient
from datetime import datetime

def date_in_str():
    now = datetime.now()
    date_format_str = "%d/%m/%Y %H:%M:%S.%f"
    date_now = now.strftime(date_format_str)
    return date_now

def str_in_date(date):
    date_format_str = "%d/%m/%Y %H:%M:%S.%f"
    return  datetime.strptime(date, date_format_str)

client = MongoClient("127.0.0.1:27017") 

client.drop_database('blog')

db=client.blog
articles = db.articles

article1 ={
    "titre" : "Simplon",
    "auteur" : "JP",
    "resumer" : "blablalbla  bla bla bla",
    "texte" : "La formation à Simplon est dure.",
    "date" : date_in_str(),
    "commentaires" : [{
        "auteur" : "Claire",
        "texte_commentaire" : "J'adore!"
    }]
}

article2 ={
    "titre" : "Les bananes",
    "auteur" : "Thomas",
    "resumer" : "blablalbla  bla bla bla",
    "texte" : "Les bananes sont délicieuses.",
    "date" : date_in_str(),
    "commentaires" : [{
        "auteur" : "Paul",
        "texte_commentaire" : "C'est instructif!"
    }]
}

articles.insert_many([article1, article2])

for article in articles.find():
    print(article)

#Lire un article précis
print(articles.find_one({"titre" : "Les bananes"}))