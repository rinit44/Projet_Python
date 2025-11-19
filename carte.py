import random 

Deck_player1 = []
Deck_player2 = []
Deck_Card = 7 

Card = {}
Color = ['Red', 'Green', 'Blue', 'Yellow']
Value = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
special = ['2', '4']


def create_deck(): 
    global Deck_player1, Deck_player2, Deck_Card, Color, Value, special
    # Joueur 1 
    NB_special1 =  random.randint(0, 2)
    for i in range(Deck_Card-NB_special1): 
        color_choice = random.choice(Color)
        card_choice = random.choice(Value)
        Deck_player1.append((color_choice, card_choice)) 
    for i in range(NB_special1): 
        special = random.choice(special)
        Deck_player1.append(('Black', special))
    # Joueur 2
    NB_special2 =  random.randint(0, 2) 
    for i in range(Deck_Card-NB_special2): 
        color_choice = random.choice(Color)
        card_choice = random.choice(Value)
        Deck_player2.append((color_choice, card_choice))
    for i in range(NB_special2): 
        special = random.choice(special)
        Deck_player2.append(('+', special))



create_deck()
print("Joueur 1 :", Deck_player1)
print("Joueur 2 :", Deck_player2)
