import csv
import os
from flask import Flask, render_template, redirect
from flask import request, session
from datetime import datetime
import hashlib
import random
import secrets

app = Flask(__name__)
app.secret_key = "CLEPOURLOG"

Fichier_CSV = "formulaire_bts.csv"
now = datetime.now()

USERNAME = 'Corentin'
PASSWORD = 'Corentin76'
PASSWORD_HASH = 'd4cd88cdbb378b4c2c6aedd40e48029d380f450e1d384503dde2e0ceeb3f514d'


QUESTIONS = [   
    'Un zèbre est noir et ? *',
    'De quelle couleur est le lait ? *',
    'Combien font 2 + 2 ? *',
    'Quelle est la première lettre de l’alphabet ? *',
    'Combien de côtés a un carré ? *'
]

RESPONSES = {
    0: 'blanc',
    1: 'blanc',
    2: '4',
    3: 'A',
    4: '4'
}

# a supprimer
@app.route("/hash")
def hash_password():
    content = PASSWORD
    hash_object = hashlib.sha256(content.encode('utf-8'))  
    hex_dig = hash_object.hexdigest()
    return f"Pass : {hex_dig}"


@app.route('/')
def accueil():
    question_au_pif = random.choice(QUESTIONS)
    numero = QUESTIONS.index(question_au_pif)
    token_formulaire = secrets.token_hex(16)
    session['token_formulaire'] = token_formulaire

    return render_template('index.html', QUESTION=question_au_pif, numero=numero, token_formulaire=token_formulaire)



@app.route('/bonjour', methods=['GET', 'POST'])
def bonjour_post():
    if request.method == 'POST':
        token_formulaire = request.form.get('token_formulaire')
        if "token_formulaire" in session and session['token_formulaire'] == token_formulaire:
            nom = request.form['nom']
            email = request.form['email']
            email2 = request.form['email_add']
            question = request.form['reponse'].lower()
            tel = request.form['telephone']
            message = request.form['message'].replace("\r\n", " ")
            question_posée = int(request.form['question_posée'])
            ip = request.remote_addr

            if email2 == "" and RESPONSES.get(question_posée).lower() == question:
                date = now.date()
                heure = f"{now.hour}:{now.minute}:{now.second}"

                listeMessages = [{"nom": nom, "email": email, "email_add": email2, "tel": tel, "message": message, "date": date, "heure": heure, "ip":ip}]

                with open(Fichier_CSV, mode='a', newline='', encoding='UTF-8') as csvfile:
                    writer = csv.DictWriter(csvfile, listeMessages[0].keys())
                    writer.writerows(listeMessages)
                    if ip == 2 in 'formulaire_bts.csv':
                        return 'Vous avez demander trop de fois'

            print(f"nom : {nom}")
            print(f"email : {email}")
            print(f"Numéro de téléphone : {tel}")
            print(f"Message : {message}")

        else:
            return "Erreur : Jeton formulaire invalide"

    return redirect("/")



@app.route('/visualisation')
def afficher_csv():

    #tester si on est logué
    if "authentifie" in session and session['authentifie'] == 'oui':
            donnee_csv = []
            #si log
            with open ('formulaire_bts.csv' , 'r') as file:
                csv_lecture = csv.reader(file)
                for row in csv_lecture:
                    donnee_csv.append(row)                
            return render_template('visualisation.html', donnee_csv=donnee_csv)
    else: 
        return redirect("/login")


@app.route('/login')
def login():
    return render_template('login.html')
    
@app.route('/connect', methods=['GET'])
def connect():
    if request.method == 'GET':
        password = request.args.get('password')
        login = request.args.get('login')

        print(f"password : {password}")
        print(f"login : {login}")

        # Generate hash 
        verify_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

        # Compare hashes
        if verify_hash == PASSWORD_HASH and login == USERNAME:
            session["authentifie"] = 'oui'
            return redirect("/visualisation")
        else:
            session["authentifie"] = 'non'

    return redirect("/login")


@app.route('/disconnect', methods=['GET'])
def disconnect():
    session["authentifie"] = 'non'
    return redirect("/login")


@app.route('/base')
def base():
    return render_template('base.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)


 # Filigrane caché (Base64) :
# Q2UgY29kZSBhIGV0w6kgcmVhbGlzZSBwYXIgUlVFVFRFIENvcmVudGlu
   