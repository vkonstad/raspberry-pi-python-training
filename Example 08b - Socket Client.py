import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', 65432))
    s.sendall('My name is Client'.encode())
    data = s.recv(1024)
    print(f"Received {data!r}")