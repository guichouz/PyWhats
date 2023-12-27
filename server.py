import socket
import threading

# Fonction pour envoyer un message à tous les clients connectés
def broadcast(message):
    for client in clients:
        client.send(message)

# Gère chaque connexion client individuellement
def handle_client(client):
    while True:
        try:
            # Réception du message du client
            message = client.recv(1024)
            # Envoi du message à tous les clients
            broadcast(message)
        except:
            # En cas d'erreur, on retire le client de la liste et on ferme la connexion
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            # Informer les autres clients que ce client a quitté le chat
            broadcast(f'{nickname} a quitté le chat!'.encode('utf-8'))
            nicknames.remove(nickname)
            break

# Configuration du socket serveur
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 55555))
server.listen()

# Listes pour gérer les clients et leurs pseudonymes
clients = []
nicknames = []

# Boucle principale pour accepter les connexions
while True:
    client, address = server.accept()
    print(f"Connecté avec {str(address)}")

    # Demande au client son pseudonyme
    client.send('NICK'.encode('utf-8'))
    nickname = client.recv(1024).decode('utf-8')
    nicknames.append(nickname)
    clients.append(client)

    print(f'Le pseudonyme du client est {nickname}!')
    # Informer tous les clients qu'un nouveau client a rejoint
    broadcast(f'{nickname} a rejoint le chat!'.encode('utf-8'))
    client.send('Connecté au serveur!'.encode('utf-8'))
    client.send(''.encode('utf-8'))

    # Démarrer un nouveau thread pour gérer la connexion avec ce client
    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()
