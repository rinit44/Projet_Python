"""Example snippets to integrate discovery/server into your existing `start.py`.

This file is only an example: it does not alter your existing UI code. Use the
snippets below inside your menu logic to show discovered servers or host a game.
"""

# Example: start a scanner thread and provide a callback to update UI list
from network_discovery import ClientScanner, ServerAnnouncer
from network_server import GameServer
from network_client import connect_to_server
import threading
import time

# shared list (safe-ish for simple UI use)
available_games = []


def on_update(servers):
    # servers is a list of dicts from discovery payloads
    global available_games
    available_games = servers


def start_scanner():
    scanner = ClientScanner(on_update=on_update)
    scanner.start()
    return scanner


def stop_scanner(scanner):
    scanner.stop()


def host_game(tcp_port=50000, name='UNO Host'):
    # start TCP game server
    server = GameServer(host='', port=tcp_port)
    server.start()
    # start announcer
    announcer = ServerAnnouncer(tcp_port=tcp_port, name=name)
    announcer.start()
    return server, announcer


def join_game_from_payload(payload):
    # payload expected to contain 'ip' and 'port'
    ip = payload.get('ip')
    port = int(payload.get('port'))
    sock = connect_to_server(ip, port)
    # receive initial welcome
    from network_client import recv_message
    msg = recv_message(sock)
    return sock, msg


if __name__ == '__main__':
    # quick demo: start a scanner, print found games every second
    sc = start_scanner()
    try:
        for _ in range(10):
            print('Available games:', available_games)
            time.sleep(1)
    finally:
        stop_scanner(sc)
