import socket

hote = 'localhost'
port = 12800

# On définit le socket pour une connexion TCP
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# On se connecte au serveur
connexion_avec_serveur.connect((hote, port))
print("La connexion avec le serveur a été établie sur le port", port)

msg_envoyé = b""
while msg_envoyé != b"fin":
    msg_envoyé = input("> ")
    msg_envoyé = msg_envoyé.encode()

    connexion_avec_serveur.send(msg_envoyé)

    #Attente de la réponse du serveur
    msg_reçu = connexion_avec_serveur.recv(1024)
    print(msg_reçu.decode())

# On ferme la connexion avec le serveur
print("Fermeture de la connexion")
connexion_avec_serveur.close()
