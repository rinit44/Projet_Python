import socket
import threading
import time

TCP_PORT = 50000


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


class GameServer:
    """Simple TCP server to accept connections from clients.

    The server uses a very small protocol: each message is prefixed by a 4-byte
    big-endian length. This is easy to integrate and avoids TCP fragmentation issues.
    """

    def __init__(self, host='', port=TCP_PORT):
        self.host = host
        self.port = int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        self._stop = threading.Event()

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        threading.Thread(target=self._accept_loop, daemon=True).start()

    def stop(self):
        self._stop.set()
        try:
            self.sock.close()
        except Exception:
            pass
        for c in list(self.clients):
            try:
                c.close()
            except Exception:
                pass
        self.clients.clear()

    def _accept_loop(self):
        while not self._stop.is_set():
            try:
                conn, addr = self.sock.accept()
                self.clients.append(conn)
                threading.Thread(target=self._handle_client, args=(conn, addr), daemon=True).start()
            except Exception:
                break

    def _handle_client(self, conn, addr):
        try:
            # send a welcome message (length-prefixed)
            self.send_message(conn, b"HELLO_FROM_SERVER")
            while not self._stop.is_set():
                data = self.recv_message(conn)
                if data is None:
                    break
                # Here you would handle messages (join, play card, etc.)
                # For now we just echo received messages to all clients.
                self.broadcast(data)
        except Exception:
            pass
        finally:
            try:
                conn.close()
            except Exception:
                pass
            if conn in self.clients:
                self.clients.remove(conn)

    def send_message(self, conn, data: bytes):
        try:
            length = len(data).to_bytes(4, 'big')
            conn.sendall(length + data)
        except Exception:
            pass

    def recv_message(self, conn, timeout=0.1):
        conn.settimeout(timeout)
        try:
            header = conn.recv(4)
            if not header or len(header) < 4:
                return None
            length = int.from_bytes(header, 'big')
            buf = b''
            while len(buf) < length:
                chunk = conn.recv(length - len(buf))
                if not chunk:
                    return None
                buf += chunk
            return buf
        except socket.timeout:
            return b''  # no data this cycle
        except Exception:
            return None

    def broadcast(self, data: bytes):
        for c in list(self.clients):
            try:
                self.send_message(c, data)
            except Exception:
                pass


if __name__ == '__main__':
    srv = GameServer(host=get_local_ip(), port=TCP_PORT)
    srv.start()
    print('Server started on', get_local_ip(), 'port', TCP_PORT)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        srv.stop()
