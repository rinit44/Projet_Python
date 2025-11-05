# Nom : test.py
# Auteur : Rinit Krasniqi, Rodrigo Fernandes Valente
# Date : 05.11.2025
import random
import os 
import pygame
import sys
os.system('cls' if os.name == 'nt' else 'clear')
Card_List = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
Color_Cards = ["Rouge", "Bleu", "Vert", "Jaune"]
Special_Cards = ["+2", "+4", "Passe ton tour"]

def gen_card(): 
    id = random.randint(1,2)    
    if id == 1: 
        for i in range(5):
            a = random.choice(Card_List)
            b = random.choice(Color_Cards)
            print(f"Couleur : {b} | Carte : {a}")
        for i in range(2): 
            c = random.choice(Special_Cards)
            print(f"Carte Spéciale : {c}")
    else: 
        for i in range(7): 
            a = random.choice(Card_List)
            b = random.choice(Color_Cards)
            print(f"Couleur : {b} | Carte : {a}")



#========================================
#=========PYGAME SECTION=================
#========================================
pygame.init()
Largeur_fenetre = 800
Hauteur_fenetre = 1000
fenetre = pygame.display.set_mode((Largeur_fenetre, Hauteur_fenetre))

# --- Couleurs ---
bg_color = (50, 143, 168)
couleur_rond = (255, 0, 0)  
while True:
    # Gestion des événements clavier souris fermeture
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    fenetre.fill(bg_color)  # On efface l’écran
    pygame.draw.circle(fenetre, couleur_rond, (400, 300), 50)  

    pygame.display.flip()  # Met à jour la fenêtre

gen_card()

