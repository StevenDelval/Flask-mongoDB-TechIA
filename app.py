from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)

@app.route("/")
def accueil():
    return render_template("accueil.html")

@app.route('/article/<nom>')
def article(nom):
    return render_template("article.html", nom=nom)
