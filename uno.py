# Nom : test.py
# Auteur : Rinit Krasniqi, Rodrigo Fernandes Valente
# Date : 05.11.2025
import random
import os 

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
        
gen_card()

