Voici ton texte reformatté **en style README GitHub**, **sans rien changer au contenu**, uniquement la mise en forme :

---

# Dual UNO – Projet Python

## Groupe :

* Rodrigo
* Rinit

## Nom du Projet :

**Dual UNO**

## Description :

Dual UNO est un jeu de cartes UNO développé en Python avec Pygame, jouable à deux.
Chaque joueur possède son propre poste, et le jeu communique en localhost.

L’objectif est de proposer une version complète et fluide du UNO classique avec une interface graphique simple et des règles officielles.

## Fonctionnalités :

* Gestion des cartes du UNO : couleurs, valeurs, cartes spéciales
* Règles officielles (couleur, valeur, piocher si non-jouable, etc.)
* Distribution automatique : 7 cartes initiales par joueur

### Cartes spéciales supportées :

* +2
* +4
* Changement de couleur
* Passer son tour

## Interface graphique Pygame :

* Affichage des cartes
* Carte centrale visible
* Mode Duel sur réseau local
* Communication client/serveur
* Synchronisation des cartes jouées

## Scénario d'utilisation :

1. Chaque joueur reçoit 7 cartes distribuées aléatoirement.
2. Une carte est placée au centre pour commencer.
3. À son tour, le joueur :

   * joue une carte si elle correspond en couleur ou en valeur
   * ou joue une carte spéciale compatible
4. S'il ne peut pas jouer → pioche une carte
5. Si la carte piochée est jouable → il peut la poser immédiatement


### Diagramme de flux :

(https://github.com/rinit44/Projet_Python/blob/main/MA-24_UNO_projet_python.drawio)

### Exemple :

Carte centrale = **Rouge 5**
Le joueur peut jouer :

* toute carte Rouge
* toute carte 5
* ou une carte spéciale (ex. +4)

## Dépendances :

```
pip install pygame
```

---

