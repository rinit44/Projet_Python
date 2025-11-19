import pygame
import threading
import json
import time

from network_client import send_message, recv_message, connect_to_server


def Game_interface(screen, sock=None):
    """Simple networked demo: each client controls a pixel with WASD.

    If `sock` is provided it must be a connected socket object. The client
    will send JSON messages {"type":"pos","x":X,"y":Y} and listen for
    other clients' messages to draw their pixels.
    """
    pygame.init()
    clock = pygame.time.Clock()
    w, h = screen.get_size()

    local_id = str(time.time())
    local_pos = [w // 2, h // 2]
    peers = {}  # id -> (x,y)

    running = True

    socket_lock = threading.Lock()

    def recv_loop(s):
        # read length-prefixed messages using recv_message helper
        while running:
            try:
                data = recv_message(s)
                if data is None:
                    break
                if data == b'':
                    time.sleep(0.01)
                    continue
                try:
                    payload = json.loads(data.decode('utf-8'))
                    if payload.get('type') == 'pos':
                        pid = payload.get('id')
                        if pid and pid != local_id:
                            peers[pid] = (int(payload.get('x', 0)), int(payload.get('y', 0)))
                except Exception:
                    pass
            except Exception:
                break

    recv_thread = None
    if sock is not None:
        recv_thread = threading.Thread(target=recv_loop, args=(sock,), daemon=True)
        recv_thread.start()

    font = pygame.font.Font(None, 24)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        moved = False
        if keys[pygame.K_w]:
            local_pos[1] -= 4; moved = True
        if keys[pygame.K_s]:
            local_pos[1] += 4; moved = True
        if keys[pygame.K_a]:
            local_pos[0] -= 4; moved = True
        if keys[pygame.K_d]:
            local_pos[0] += 4; moved = True

        # clamp
        local_pos[0] = max(0, min(w-1, local_pos[0]))
        local_pos[1] = max(0, min(h-1, local_pos[1]))

        if moved and sock is not None:
            msg = json.dumps({'type': 'pos', 'id': local_id, 'x': local_pos[0], 'y': local_pos[1]}).encode('utf-8')
            try:
                with socket_lock:
                    send_message(sock, msg)
            except Exception:
                pass

        # draw
        screen.fill((30, 30, 30))
        # draw peers
        for pid, (x, y) in peers.items():
            pygame.draw.rect(screen, (255, 80, 80), (x-4, y-4, 8, 8))
            label = font.render(pid[-4:], True, (200,200,200))
            screen.blit(label, (x+6, y-6))

        # draw local
        pygame.draw.rect(screen, (80, 200, 80), (local_pos[0]-5, local_pos[1]-5, 10, 10))
        label = font.render('You', True, (200,200,200))
        screen.blit(label, (local_pos[0]+6, local_pos[1]-6))

        pygame.display.flip()
        clock.tick(60)

    # cleanup
    try:
        if sock is not None:
            try:
                sock.close()
            except Exception:
                pass
    except Exception:
        pass

    pygame.quit()
