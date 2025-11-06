import pygame
import sys
import random
import os
import socket
import threading
import json

# -----------------------------------------------------------
# Menu pour ce connecter au réseai
# -----------------------------------------------------------
print("=== UNO LAN ===")
print("1) Héberger une partie")
print("2) Se connecter à une partie")

choix = input("Votre choix : ")

if choix == "1":
    MODE = "host"
    host = socket.gethostbyname(socket.gethostname())
    HOST_IP = "0.0.0.0"
    PORT = 5000
    print(f"Adresse IP du serveur : {host}")
elif choix == "2":
    MODE = "client"
    HOST_IP = input("IP du serveur : ")
    PORT = 5000
else:
    print("Choix invalide.")
    sys.exit()

# -----------------------------------------------------------
# CHAT GPT => Socket pour sycro les carte 
# -----------------------------------------------------------

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send_json(data):
    sock.send(json.dumps(data).encode() + b"\n")

def recv_json():
    data = sock.recv(4096).decode().strip()
    return json.loads(data)


if MODE == "host":
    sock.bind((HOST_IP, PORT))
    sock.listen()
    print("En attente du joueur...")
    conn, addr = sock.accept()
    sock = conn
    player_id = 1
else:
    sock.connect((HOST_IP, PORT))
    player_id = 2

# -----------------------------------------------------------
# START LE FICHIER PYTHON 
# -----------------------------------------------------------
pygame.init()
LARGEUR, HAUTEUR = 800, 1000
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Uno LAN")
font = pygame.font.Font(None, 36)
BG_COLOR = (50, 143, 168)

# -----------------------------------------------------------
#  STOCKET LES CARTE 
# -----------------------------------------------------------
COULEURS = ["Rouge", "Bleu", "Vert", "Jaune"]
VALEURS = ["1","2","3","4","5","6","7","8","9"]
SPECIALS = ["+2", "+4"]

images_cartes = {}

for couleur in COULEURS + ["Spéciale"]:
    images_cartes[couleur] = {}
    folder = f"img/{couleur.lower()}" if couleur != "Spéciale" else "img/special"
    if os.path.exists(folder):
        for fichier in os.listdir(folder):
            if fichier.endswith(".png"):
                nom_carte = os.path.splitext(fichier)[0]
                chemin = os.path.join(folder, fichier)
                img = pygame.image.load(chemin).convert_alpha()
                images_cartes[couleur][nom_carte] = pygame.transform.smoothscale(img, (100, 150))

pioche_img = None
if os.path.exists("img/logo.png"):
    img = pygame.image.load("img/logo.png").convert_alpha()
    pioche_img = pygame.transform.smoothscale(img, (100, 150))


def generer_main():
    main = []
    nb_special = random.randint(0, 2)
    for _ in range(nb_special):
        main.append({"couleur": "Spéciale", "carte": random.choice(SPECIALS)})
    while len(main) < 7:
        couleur = random.choice(COULEURS)
        valeur = random.choice(VALEURS)
        main.append({"couleur": couleur, "carte": valeur})
    random.shuffle(main)
    return main

def generer_carte_centrale():
    valeur = random.choice(VALEURS + SPECIALS)
    couleur = "Spéciale" if valeur in SPECIALS else random.choice(COULEURS)
    return {"couleur": couleur, "carte": valeur}

def draw_carte(carte, x, y):
    couleur = carte["couleur"]
    valeur = carte["carte"]
    if couleur in images_cartes and valeur in images_cartes[couleur]:
        fenetre.blit(images_cartes[couleur][valeur], (x, y))
    else:
        pygame.draw.rect(fenetre, (255,255,255), (x,y,100,150))
        text = font.render(valeur, True, (0,0,0))
        fenetre.blit(text, (x+20, y+60))

# -----------------------------------------------------------
# # ENCOYER LES CARTE SUR LES DEUX POST 
# -----------------------------------------------------------

if player_id == 1:
    user1 = generer_main()
    user2 = generer_main()
    central = generer_carte_centrale()

    send_json({
        "user1": user1,
        "user2": user2,
        "central": central
    })
else:
    data = recv_json()
    user1 = data["user1"]
    user2 = data["user2"]
    central = data["central"]

# -----------------------------------------------------------
# # Garder la fenêtre ouverte
# -----------------------------------------------------------

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    fenetre.fill(BG_COLOR)

    # -----------------------------------------------------------
    # voir les même carte 
    # -----------------------------------------------------------

    if player_id == 1:
        x, y = 20, 20
        for carte in user1:
            draw_carte(carte, x, y)
            x += 110
        x, y = 20, HAUTEUR - 170
        for _ in user2:
            fenetre.blit(pioche_img, (x, y))
            x += 110

    else:
        x, y = 20, HAUTEUR - 170
        for carte in user2:
            draw_carte(carte, x, y)
            x += 110
        x, y = 20, 20
        for _ in user1:
            fenetre.blit(pioche_img, (x, y))
            x += 110
    # Carte de pioche centrale
    central_x = (LARGEUR - 100)//2
    central_y = (HAUTEUR - 150)//2
    draw_carte(central, central_x, central_y)

    # Pioche
    if pioche_img:
        fenetre.blit(pioche_img, (central_x - 130, central_y))

    pygame.display.flip()
