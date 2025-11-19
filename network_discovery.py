import socket
import threading
import json
import time

DISCOVERY_PORT = 37020
BROADCAST_INTERVAL = 1.0


def get_local_ip():
    """Return the local IP address (not 127.0.0.1) when possible."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


class ServerAnnouncer(threading.Thread):
    """Periodically broadcast a JSON service announcement on the LAN.

    Usage:
        ann = ServerAnnouncer(tcp_port=50000, name='My UNO')
        ann.start()
        ann.stop()
    """

    def __init__(self, tcp_port, name="UNO", interval=BROADCAST_INTERVAL):
        super().__init__(daemon=True)
        self.tcp_port = int(tcp_port)
        self.name = name
        self.interval = interval
        self._stop = threading.Event()
        self.ip = get_local_ip()

    def stop(self):
        self._stop.set()

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        payload = json.dumps({"ip": self.ip, "port": self.tcp_port, "name": self.name}).encode("utf-8")
        while not self._stop.is_set():
            try:
                sock.sendto(payload, ("<broadcast>", DISCOVERY_PORT))
            except Exception:
                # ignore send errors (network down, no permission...)
                pass
            time.sleep(self.interval)
        sock.close()


class ClientScanner(threading.Thread):
    """Listen for UDP broadcasts and keep a list of discovered servers.

    - on_update callback receives a list of server dicts
    - call stop() to terminate the background thread
    """

    def __init__(self, on_update=None, ttl=5.0):
        super().__init__(daemon=True)
        self.on_update = on_update
        self._stop = threading.Event()
        self.found = {}  # key=(ip,port) -> (payload, last_seen)
        self.ttl = ttl

    def stop(self):
        self._stop.set()

    def get_servers(self):
        """Return a list of payload dicts currently considered alive."""
        now = time.time()
        out = []
        for key, (payload, seen) in list(self.found.items()):
            if now - seen <= self.ttl:
                out.append(payload)
            else:
                del self.found[key]
        return out

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("", DISCOVERY_PORT))
        except Exception:
            # If bind fails, try binding to localhost only
            sock.bind(("127.0.0.1", DISCOVERY_PORT))
        sock.settimeout(1.0)
        while not self._stop.is_set():
            try:
                data, addr = sock.recvfrom(2048)
                try:
                    payload = json.loads(data.decode("utf-8"))
                    key = (payload.get("ip", addr[0]), int(payload.get("port", 0)))
                    self.found[key] = (payload, time.time())
                    if self.on_update:
                        self.on_update(self.get_servers())
                except Exception:
                    # ignore malformed payloads
                    pass
            except socket.timeout:
                # periodic cleanup callback
                if self.on_update:
                    self.on_update(self.get_servers())
                continue
        sock.close()


def discover_blocking(timeout=2.0):
    """Blocking discovery helper: listen for `timeout` seconds and return found services."""
    results = {}
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", DISCOVERY_PORT))
    sock.settimeout(timeout)
    t0 = time.time()
    try:
        while time.time() - t0 < timeout:
            try:
                data, addr = sock.recvfrom(2048)
                payload = json.loads(data.decode("utf-8"))
                key = (payload.get("ip", addr[0]), int(payload.get("port", 0)))
                results[key] = payload
            except socket.timeout:
                break
            except Exception:
                continue
    finally:
        sock.close()
    return list(results.values())
