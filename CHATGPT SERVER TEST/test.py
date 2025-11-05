import pygame, sys

pygame.init()
fenetre = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Affichage de formes et texte")

# Couleurs
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
NOIR = (0, 0, 0)

# Police et texte
police = pygame.font.Font(None, 50)  # None = police par défaut, 50 = taille
texte_surface = police.render("Bonjour Pygame !", True, BLEU)  # True = lissage (anti-aliasing)
texte_rect = texte_surface.get_rect(center=(400, 50))  # Position centrée en haut

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    fenetre.fill(BLANC)  # fond blanc

    # --- Formes ---
    pygame.draw.rect(fenetre, ROUGE, (100, 150, 150, 100))          # rectangle
    pygame.draw.circle(fenetre, VERT, (400, 300), 60)               # cercle
    pygame.draw.ellipse(fenetre, BLEU, (550, 400, 150, 80))         # ellipse
    pygame.draw.line(fenetre, NOIR, (0, 0), (800, 600), 5)          # ligne diagonale

    # --- Texte ---
    fenetre.blit(texte_surface, texte_rect)

    pygame.display.flip()
