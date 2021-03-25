import socket
import select

#constants
HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 3000

#set the server socket to allow multiple connections by allowing address reuse
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#open the server socket for connections
server_socket.bind((IP, PORT))
server_socket.listen()
