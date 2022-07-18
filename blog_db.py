from pymongo import MongoClient

client = MongoClient("127.0.0.1:27017") 

client.drop_database('blog')

db=client.blog
articles = db.articles

article1 ={
    "titre" : "Simplon",
    "auteur" : "JP",
    "contenu" : "La formation à Simplon est dure.",
    "commentaires" : [{
        "auteur" : "Claire",
        "texte_commentaire" : "J'adore!"
    }]
}

article2 ={
    "titre" : "Les bananes",
    "auteur" : "Thomas",
    "contenu" : "Les bananes sont délicieuses.",
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