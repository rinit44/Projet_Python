import pygame
import main 
pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.Font(None, 40)
print(main.global_staus)
# Position et taille du bouton
button_rect = pygame.Rect(300, 250, 200, 80)
btn_stop = pygame.Rect(300, 250, 200, 80)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Détection du clic
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                main.global_staus = 1 
                print(main.global_staus)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_stop.collidepoint(event.pos):
                running = False
    screen.fill("white")

    # Dessiner le bouton
    pygame.draw.rect(screen, "blue", button_rect, border_radius=10)
    pygame.draw.rect(screen, "red", btn_stop, border_radius=10)

    # Texte du bouton
    text = font.render("Jouer", True, "white")
    screen.blit(text, (button_rect.x + 50, button_rect.y + 20))
    text_stop = font.render("Quitter", True, "white")
    screen.blit(text_stop, (btn_stop.x + 50, btn_stop.y + 20))

    pygame.display.flip()

pygame.quit()
