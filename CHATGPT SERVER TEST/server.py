import socket

# --- Étape 1 : Configurer le serveur ---
# Obtenir l'adresse IP locale de la machine
host = socket.gethostbyname(socket.gethostname())
port = 5000  # Choisir un port libre (>=1024)

print(f"Adresse IP du serveur : {host}")
print("En attente de connexion...")

# --- Étape 2 : Créer la socket ---
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)  # Attendre 1 client

# --- Étape 3 : Accepter une connexion ---
conn, addr = server_socket.accept()
print(f"Connexion établie avec {addr}")

# --- Étape 4 : Communication ---
while True:
    data = conn.recv(1024).decode()
    if not data or data.lower() == "quit":
        print("Connexion fermée par le client.")
        break
    print(f"Client : {data}")
    message = input("Serveur : ")
    conn.send(message.encode())
    if message.lower() == "quit":
        break

# --- Étape 5 : Fermer ---
conn.close()
server_socket.close()
