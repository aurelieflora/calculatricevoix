from flask import Flask, render_template, request, session, redirect, url_for, flash
import speech_recognition as sr
from gtts import gTTS
from flaskext.mysql import MySQL
from datetime import datetime
import os
import wave
import sys
import pyttsx3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'calculatrice'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculer', methods=['POST'])
def calculer():
    # Code de traitement des données du formulaire
    # Renvoi du résultat calcul
    return render_template('calculer.html')


def effacer(liste):
    del liste[:]


historique_calculs = []


def effacer(liste):
    liste.clear()


@app.route('/traiter', methods=['POST'])
def traiter():
    global historique_calculs
    texte_vocal = request.form['texte_vocal']
    if "effacer" in texte_vocal.lower():
        effacer(historique_calculs)
        return "Effacé."
    try:
        # Remplacement de la virgule par un point pour les nombres à virgule
        texte_vocal = texte_vocal.replace(',', '.')
        # Ajout de la possibilité de calculer des pourcentages
        if "%" in texte_vocal:
            expression = texte_vocal.replace('%', '/100')
            resultat = str(eval(expression))
        else:
            resultat = str(round(eval(texte_vocal), 2))
        # Enregistrement dans la base de données
        cnx = mysql.connect()
        cursor = cnx.cursor()
        insert_query = "INSERT INTO history (calcul, resultat) VALUES (%s, %s)"
        cursor.execute(insert_query, (texte_vocal, resultat))
        cnx.commit()
        cursor.close()
        cnx.close()
        historique_calculs.append(
            (cursor.lastrowid, texte_vocal, resultat, datetime.now()))
        # Conversion du résultat en audio et lecture
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(resultat)
        engine.runAndWait()
    except:
        resultat = "Désolé, je n'ai pas compris. Veuillez réessayer."
    return resultat


@app.route('/history', methods=['GET', 'POST'])
def history():
    global historique_calculs
    cnx = mysql.connect()
    cursor = cnx.cursor()
    select_query ="SELECT * FROM history ORDER BY date DESC"
    cursor.execute(select_query)
    historique_calculs = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('history.html', historique_calculs=historique_calculs)


if __name__ == '__main__':
    app.run(debug=True)
