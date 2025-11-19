Network discovery + simple TCP game server for UNO

Files added:
- network_discovery.py : UDP broadcast announcer + scanner
- network_server.py    : simple TCP server with length-prefixed messages
- network_client.py    : helpers to connect/send/receive
- network_integration_example.py : snippets to integrate into your `start.py`

Integration notes:
- To host a game: run GameServer and ServerAnnouncer (see example).
- To join a game: run ClientScanner in a background thread and show the
  discovered servers to the player. When the player picks one, call
  connect_to_server(ip, port).

Security / Windows notes:
- On Windows you may need to allow Python through the firewall for the chosen ports.
- UDP broadcast may not work across different subnets or if the network blocks broadcasts.

If you want, I can now patch `start.py` to start the scanner and render the list of
available games in the menu (no major logic changes, only adding a small thread).
