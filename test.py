# Nom : test.py
# Auteur : Rinit Krasniqi, Rodrigo Fernandes Valente
# Date : 05.11.2025


import random

ValueList = ["1","2","3","4","5","6","7","8","9"]
ColorList =["Rouge","Vert","Bleu","Jaune"]

def playerCards():
    hand = []  # liste vide pour stocker les cartes
    for i in range(7):
        color = random.choice(ColorList)
        value = random.choice(ValueList)
        card = (color, value)
        hand.append(card)
    return hand
       
player1 = playerCards()
player2 = playerCards()

print("Cartes du Joueur 1 :")
for color, value in player1:
    print(f"Couleur : {color} | Valeur : {value}")

print("\nCartes du Joueur 2 :")
for color, value in player2:
    print(f"Couleur : {color} | Valeur : {value}")
