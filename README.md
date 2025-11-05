# Projet_Python

## Groupe
- Rodrigo
- Rinit
- ... 

## Nom du Projet
**Dual Uno**

## Description
Dual Uno est un jeu de Uno qui se joue sur **deux postes différents via un serveur sur le réseau local**. Le jeu respecte les règles classiques du Uno et permet une expérience multijoueur simple et interactive.

## Fonctionnalités
- Gestion des **7 cartes initiales** pour chaque joueur.
- Respect des **règles officielles du Uno** :  
  [Règles officielles du Uno](https://www.jeuxuno.com/regles-officielles)
- Gestion des **cartes spéciales** : +2, +4, etc.
- Affichage **graphique avec Pygame** pour les cartes et le plateau.
- Carte centrale affichée au centre du plateau.
- Overlay noir semi-transparent pour **une meilleure lisibilité des numéros**.
- Support pour les cartes de couleur et spéciales avec leurs effets.

## Scénario d'utilisation
1. Chaque joueur reçoit **7 cartes choisies aléatoirement** dans la pioche, toutes couleurs et valeurs confondues.  
2. Le joueur peut **poser une carte** si elle correspond en couleur ou en valeur à la carte sur le dessus du tas de défausse.  
3. Sinon, le joueur **pioche une carte**.  
4. Si la carte piochée est jouable, le joueur peut la **poser immédiatement**.  
5. Exemple : Si la carte du dessus de la défausse est **Rouge 5**, le joueur peut jouer **toute carte Rouge** ou **toute carte 5**, ou une carte spéciale compatible.

## Dépendances
Avant de lancer le jeu, installez **Pygame** :  

```bash
pip install pygame
