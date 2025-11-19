import pygame
from interface import Game_interface

# network helpers (created separately)
try:
    from network_discovery import ClientScanner
    from network_integration_example import host_game, start_scanner, join_game_from_payload
except Exception:
    ClientScanner = None
    host_game = None
    start_scanner = None
    join_game_from_payload = None


def Start_Game():
    pygame.init()
    pygame.display.set_caption("UNO Game")
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.Font(None, 28)
    btn_play = pygame.Rect(300, 200, 200, 60)
    btn_host = pygame.Rect(100, 200, 150, 50)
    btn_scan = pygame.Rect(100, 270, 150, 50)
    btn_stop = pygame.Rect(350, 350, 100, 40)

    # Variables de status locales
    Player1_Status = 0
    Player2_Status = 0
    global_status = 0

    # Network state
    scanner = None
    announcer_server = None
    available_games = []
    selected_server = None
    selected_sock = None

    def on_update(servers):
        nonlocal available_games
        available_games = servers

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if Player1_Status == 0 and Player2_Status == 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_play.collidepoint(event.pos):
                        # if a server is selected, hand the socket to the interface
                        try:
                            if 'selected_sock' in locals() and selected_sock is not None:
                                Game_interface(screen, selected_sock)
                            else:
                                Game_interface(screen, None)
                        except TypeError:
                            # older Game_interface signature fallback
                            Game_interface(screen)
                        running = False
                        print("Global status =", global_status)
                    if btn_stop.collidepoint(event.pos):
                        running = False
                        pygame.quit()
                    if btn_host.collidepoint(event.pos) and host_game is not None:
                        # start hosting (server + announcer)
                        server, announcer = host_game()
                        announcer_server = (server, announcer)
                    if btn_scan.collidepoint(event.pos) and start_scanner is not None:
                        if scanner is None:
                            scanner = start_scanner()
                            # replace scanner's on_update with local callback if possible
                            try:
                                scanner.on_update = on_update
                            except Exception:
                                pass
                        else:
                            scanner.stop()
                            scanner = None

            # allow clicking found games to join
            if event.type == pygame.MOUSEBUTTONDOWN and available_games:
                # simple mapping: click on listed server rectangles
                y = 420
                for idx, payload in enumerate(available_games):
                    rect = pygame.Rect(100, y + idx * 40, 400, 32)
                    if rect.collidepoint(event.pos):
                        # join selected game
                        try:
                            sock, msg = join_game_from_payload(payload)
                            print('Joined', payload, 'got', msg)
                            # select this server to play with
                            selected_server = payload
                            selected_sock = sock
                        except Exception as e:
                            print('Failed to join:', e)

        # --- Affichage ---
        screen.fill("white")

        if Player1_Status == 0 and Player2_Status == 0:
            # buttons
            pygame.draw.rect(screen, "blue", btn_play, border_radius=8)
            pygame.draw.rect(screen, "green", btn_host, border_radius=6)
            pygame.draw.rect(screen, "orange", btn_scan, border_radius=6)
            pygame.draw.rect(screen, "red", btn_stop, border_radius=10)
            text_play = font.render("PLAY", True, "white")
            text_host = font.render("HOST", True, "white")
            text_scan = font.render("SCAN", True, "white")
            text_stop = font.render("EXIT", True, "white")
            screen.blit(text_play, (btn_play.x + 80, btn_play.y + 18))
            screen.blit(text_host, (btn_host.x + 40, btn_host.y + 12))
            screen.blit(text_scan, (btn_scan.x + 40, btn_scan.y + 12))
            screen.blit(text_stop, (btn_stop.x + 20, btn_stop.y + 5))

            # show discovered games
            info = font.render("Discovered games:", True, "black")
            screen.blit(info, (100, 380))
            y = 420
            for idx, payload in enumerate(available_games):
                line = f"{payload.get('name')} - {payload.get('ip')}:{payload.get('port')}"
                txt = font.render(line, True, "black")
                screen.blit(txt, (100, y + idx * 40))
                pygame.draw.rect(screen, "#dddddd", (100, y + idx * 40, 400, 32), 1)
        else:
            Game_interface(screen)

        pygame.display.flip()

    # cleanup
    if scanner is not None:
        try:
            scanner.stop()
        except Exception:
            pass
    if announcer_server is not None:
        try:
            server, announcer = announcer_server
            announcer.stop()
            server.stop()
        except Exception:
            pass

    pygame.quit()
