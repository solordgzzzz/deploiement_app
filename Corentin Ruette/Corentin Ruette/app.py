import csv
import os
from flask import Flask, render_template, redirect
from flask import request, session
from datetime import datetime
import hashlib

app = Flask(__name__)
app.secret_key = "CLEPOURLOG"

Fichier_CSV = "Formulaire_inscription.csv"
now = datetime.now()

USERNAME = 'Corentin'
PASSWORD = 'Corentin76'
PASSWORD_HASH = "d4cd88cdbb378b4c2c6aedd40e48029d380f450e1d384503dde2e0ceeb3f514d"

# a supprimer
@app.route("/hash")
def hash_password():
    content = PASSWORD
    hash_object = hashlib.sha256(content.encode('utf-8'))  
    hex_dig = hash_object.hexdigest()
    return f"Pass : {hex_dig}"


@app.route('/')
def accueil():
    return render_template('index.html')

@app.route('/bonjour', methods=['GET', 'POST'])
def bonjour_post():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        tel = request.form['telephone']
        message = request.form['message'].replace("\r\n", " ")
        

        date = now.date()
        heure = f"{now.hour}:{now.minute}:{now.second}" 

        listeMessages = [{"nom":nom , "email":email , "tel":tel , "message":message , "date":date, "heure":heure}]

        with open(Fichier_CSV, mode='a' , newline='', encoding='UTF-8') as csvfile:
            writer = csv.DictWriter(csvfile , listeMessages[0].keys())
            #writer.writeheader()
            writer.writerows(listeMessages)


        print(f"nom : {nom}")
        print(f"email : {email}")
        print(f"Numéro de téléphone : {tel}")
        print(f"Message : {message}")


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


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nom = request.form.get('nom', '')
        prenom = request.form.get('prenom', '')
        telephone = request.form.get('telephone', '')
        email = request.form.get('email', '')
        lycee = request.form.get('lycee', '')
        classe = request.form.get('classe', '')
        ER = request.form.get('ER', 'Non') 
        IR = request.form.get('IR', 'Non')  

        date = now.date()
        heure = f"{now.hour}:{now.minute}:{now.second}"

        listeMessages = [{
            "nom": nom, "prenom": prenom, "telephone": telephone, "email": email,
            "lycee": lycee, "classe": classe, "ER": ER, "IR": IR, "date": date, "heure": heure
        }]

        
        fichier_existe = os.path.exists(Fichier_CSV)
        with open(Fichier_CSV, mode='a', newline='', encoding='UTF-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=listeMessages[0].keys())
            if not fichier_existe or os.stat(Fichier_CSV).st_size == 0:
                writer.writeheader()
            writer.writerows(listeMessages)

        return redirect("/")

    return render_template("contact.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)


 # Filigrane caché (Base64) :
# Q2UgY29kZSBhIGV0w6kgcmVhbGlzZSBwYXIgUlVFVFRFIENvcmVudGlu
   