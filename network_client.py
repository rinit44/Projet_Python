import socket
import struct

def connect_to_server(ip, port, timeout=5):
    s = socket.create_connection((ip, int(port)), timeout=timeout)
    return s


def send_message(sock, data: bytes):
    try:
        length = len(data).to_bytes(4, 'big')
        sock.sendall(length + data)
    except Exception:
        raise


def recv_message(sock):
    try:
        header = sock.recv(4)
        if not header or len(header) < 4:
            return None
        length = int.from_bytes(header, 'big')
        buf = b''
        while len(buf) < length:
            chunk = sock.recv(length - len(buf))
            if not chunk:
                return None
            buf += chunk
        return buf
    except Exception:
        return None


if __name__ == '__main__':
    # quick manual test (requires a server running)
    import sys
    if len(sys.argv) < 3:
        print('Usage: network_client.py <ip> <port>')
    else:
        ip = sys.argv[1]
        port = int(sys.argv[2])
        s = connect_to_server(ip, port)
        data = recv_message(s)
        print('Received:', data)
        s.close()
