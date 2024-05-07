import socket
import threading

HOST = 'localhost'    
PORT = 44444              

class ChatroomClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.create_connection((server_host, server_port))
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, message):
        self.client_socket.sendall(message.encode())

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                print(data.decode())
            except:
                break

    def disconnect(self):
        self.client_socket.close()

# Usage example:
if __name__ == "__main__":
    client = ChatroomClient(HOST, PORT)  # Replace with your server's host and port
    while True:
        message = input("Enter message: ")
        if message.lower() == "exit":
            break
        client.send_message(message)
    client.disconnect()
