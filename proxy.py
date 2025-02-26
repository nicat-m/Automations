import socket
import threading

def handle_client(client_socket):
    target_host = "your_ip"
    target_port = 443

    # Create a socket to the target server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((target_host, target_port))

    # Start a thread to forward data from client to server
    client_to_server_thread = threading.Thread(target=forward_data, args=(client_socket, server_socket))
    client_to_server_thread.start()

    # Forward data from server to client
    forward_data(server_socket, client_socket)

    # Close both sockets
    client_socket.close()
    server_socket.close()

def forward_data(source_socket, destination_socket):
    data = source_socket.recv(4096)
    while data:
        destination_socket.send(data)
        data = source_socket.recv(4096)

def start_proxy():
    bind_address = "0.0.0.0"
    bind_port = 443

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_address, bind_port))
    server.listen(5)

    print(f"[*] Listening on {bind_address}:{bind_port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_proxy()
