# Example 11a - Socket Server
# A TCP echo server: it sends back whatever a client sends. Start it first,
# then run "Example 11b - Socket Client.py". Stop it with Ctrl+C.
#
# Concepts: TCP sockets, bind/listen/accept, bytes, context managers

import socket

PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', PORT))          # '' = listen on all network interfaces
    s.listen()
    print(f"Listening on port {PORT} (Ctrl+C to stop)")
    try:
        while True:
            conn, addr = s.accept()     # waits here until a client connects
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:        # empty data = the client closed the connection
                        break
                    print(data)
                    conn.sendall(data)
    except KeyboardInterrupt:
        print("Server stopped")
