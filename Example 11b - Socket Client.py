# Example 11b - Socket Client
# Sends a message to the echo server of Example 11a and prints the reply.
# Run:  python "Example 11b - Socket Client.py" [server_ip]
# Without an argument it talks to the same machine; give the Pi's IP to talk across the network.
#
# Concepts: TCP client, connect, sendall/recv, encode() to turn text into bytes

import socket
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall('My name is Client'.encode())
    data = s.recv(1024)
    print(f"Received {data!r}")
