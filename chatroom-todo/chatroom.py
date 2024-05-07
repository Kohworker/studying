import socket
import threading

#issues with closing all telnet connections.  Look into and writing separate python client py file

"""
Server with socket must do the following
1. socket()
2. bind()
3. listen()
4. accept() (maybe as a repeat)

Client must do the following
1. socket()
2. connect()

1. Connect websocket to localhost and port x
- websocket is bidirectional
2. Function to handle data from client from socket
3. collect list of all clients
4. broadcast messages to all clients
5. try catches for issues with this
"""

HOST = "localhost"
PORT = 44444

clients = []


def handle_clients(client_socket, client_address) :

    try: 
        while True:
            #receive data from client
            data = client_socket.recv(1024)
            if not data : break

            print("Message from {}".format(client_address))

            msg_cleanup = "Message from {} : {}\n".format(client_address, data.decode())
            for client in clients:
                if client != client_socket:
                    
                    client.sendall(msg_cleanup.encode())
    except OSError as e:
        print("Error with {} occured with {}".format(e.errno, client_address))


def start_server():
    server_socket = socket.socket()
    server_socket.bind((HOST, PORT))

    server_socket.listen(3)
    print("Chatroom started")

    try : 
        while True:
            client_socket, client_address = server_socket.accept()
            clients.append(client_socket)

            client_thread = threading.Thread(target = handle_clients, args = (client_socket, client_address))
            print("{} has joined".format(client_address))
            client_thread.start()
    except KeyboardInterrupt:
        for client in clients : 
            client.shutdown(socket.SHUT_RDWR)
            client_socket.close()
        server_socket.shutdown(socket.SHUT_RDWR)
        server_socket.close()
    except OSError as e:
        print("Error with {} occured with {}".format(e.errno, client_address))

start_server()