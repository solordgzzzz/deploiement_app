from urllib import request, parse


data = parse.urlencode({"nom": "ATTAQUE", "email": "EN_COURS", "telephone": "DE", "message": "PROGRESSION"}).encode("utf8")
nb_envois = 5000
for i in range(nb_envois):
    res = request.urlopen("http://192.168.190.7:8000/bonjour", data=data).read()
    page = res.decode("utf8")
    print('requete envoyer')


print(data = parse.url)

