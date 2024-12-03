import socket
import threading
import json
import requests

API_KEY = "130a3a3c32144eaa95bab0c44d5668ae"
GROUP_ID = "group_A11" 
# Define the server host and port(the server will listen on this address)
#in this part the server will listen on all available network interfaces(for the client TCP socket to connect to)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080

def start_server():
    "the server will start and  listen for incoming connections"
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)  #"the server will listen for up to 5 incoming connections"
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")
