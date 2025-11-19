# UNO Pygame Demo

Petite démonstration d'une interface UNO en Pygame.

Pré-requis

- Python 3.8+
- Installer les dépendances :

```
python -m pip install -r requirements.txt
```

Lancer

```
python main.py
```

Description

- Interface minimale : main player (face up), CPU (face down), deck et discard.
- Règle simple : on peut jouer une carte si la couleur ou la valeur correspond.
- CPU très basique.

Caveats

- Pas toutes les règles UNO (cartes spéciales, +2, changement de couleur, etc.).
- Pour usage pédagogique / prototype.
