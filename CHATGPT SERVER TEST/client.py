import socket

# --- Étape 1 : Se connecter au serveur ---
# Remplacez l'adresse IP ci-dessous par celle du serveur (affichée dans son terminal)
host = input("Entrez l'adresse IP du serveur : ")
port = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
print(f"Connecté au serveur {host}:{port}")

# --- Étape 2 : Communication ---
while True:
    message = input("Client : ")
    client_socket.send(message.encode())
    if message.lower() == "quit":
        break
    data = client_socket.recv(1024).decode()
    print(f"Serveur : {data}")
    if data.lower() == "quit":
        break

# --- Étape 3 : Fermer ---
client_socket.close()
