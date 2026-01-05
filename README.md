# Dual UNO – Projet Python

## Groupe :

* Rodrigo Fernandes Valente
* Rinit Krasniqi
* Co-réal : Claude.ai

## Nom du Projet :

**Dual UNO**

## Description :

Dual UNO est un jeu de cartes UNO développé en Python avec Pygame, jouable à deux.

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
* !!! la carte spécial changer de sens n'a volontairement pas été mise car on a trouvé que ce n'était pas pertinent pour un UNO à 2 joueurs.

## Interface graphique Pygame :

* Affichage des cartes
* Carte centrale visible
* Mode Duel avec affichage de chaque deck selon le joueur

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
## Conclusion – Dual UNO
 
**Succès :**  
Le projet Dual UNO a permis de créer un jeu fonctionnel et fluide jouable à deux, respectant les règles officielles du UNO. Nous avons réussi à développer une interface graphique claire avec Pygame et à gérer correctement la logique des cartes et des tours de jeu.

---

**Échecs :**  
Certaines fonctionnalités n’ont pas été implémentées, comme la carte « changement de sens », qui aurait pu enrichir le jeu mais a été volontairement laissée de côté. Quelques ajustements graphiques et optimisations du code restent possibles.

---

**Potentialités :**  
Le projet peut évoluer vers un mode multijoueur en ligne, l’ajout d’une IA, ou des améliorations visuelles et sonores. Cette expérience ouvre la voie à d’autres projets de jeux en Python et à une meilleure maîtrise de la programmation événementielle et graphique.

---

**Obstacles :**  
La principale difficulté a été la gestion des cartes spéciales et de la logique de pioche/jeu, ainsi que la coordination entre les membres du groupe pour structurer le code. La gestion du temps et l’organisation du projet ont également été des défis à surmonter.

---

**Conclusion personnelle et de groupe :**  
Cette expérience a été très enrichissante, tant sur le plan technique que collaboratif. Elle nous a permis de travailler efficacement en groupe, de renforcer notre autonomie, et de mieux comprendre les exigences liées à la conception d’un projet logiciel complet.
