import pygame
import sys
import random
import os

pygame.init()
LARGEUR, HAUTEUR = 800, 1000
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Uno Simple")
font = pygame.font.Font(None, 36)
BG_COLOR = (50, 143, 168)
player_id = 1
# Liste des carte 
COULEURS = ["Rouge", "Bleu", "Vert", "Jaune"]
VALEURS = ["1","2","3","4","5","6","7","8","9"]
SPECIALS = ["+2","+4"]

# Stocker les images des catre 
images_cartes = {}

# charger les img 
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

# charger image pour la pioche au centre 
pioche_img = None
pioche_chemain = "img/logo.png"
if os.path.exists(pioche_chemain):
    img = pygame.image.load(pioche_chemain).convert_alpha()
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
    if valeur in SPECIALS:
        couleur = "Spéciale"
    else:
        couleur = random.choice(COULEURS)
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

# stocker carte des joueurs et la carte centreal 
user1 = generer_main()
user2 = generer_main()
central = generer_carte_centrale()

#bocule prcpl 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    fenetre.fill(BG_COLOR)

    if player_id == 1: 
        # affichier carte du plyr 1
        x = 20
        y = 20
        for carte in user1:
            draw_carte(carte, x, y)
            x += 110

        # afficher carte du plyr 2 
        x = 20
        y = HAUTEUR - 170
        for i in user2:
            fenetre.blit(pioche_img, (x, y))
            x+=110
    else: 
        # afficher carte du plyr 1 
        x = 20
        y = 20
        for i in user1:
            fenetre.blit(pioche_img, (x, y))
            x+=110

        # afficher carte du plyr 2 
        x = 20
        y = HAUTEUR - 170
        for carte in user2:
            draw_carte(carte, x, y)
            x += 110

    # afficher carte du ceentre 
    central_x = (LARGEUR - 100)//2
    central_y = (HAUTEUR - 150)//2
    draw_carte(central, central_x, central_y)

    # afficher carte de pioche 
    if pioche_img:
        fenetre.blit(pioche_img, (central_x - 130, central_y))  # 130 px à gauche de la centrale

    pygame.display.flip()
