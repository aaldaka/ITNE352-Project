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
    
    return server_socket

"the server will accept incoming connections and handle each client in a separate thread"

def handle_client(client_socket , client_address):
    "the server will handle the client connection"
    print(f"Accepted connection from {client_socket.getpeername()}")
    
    try:
        #here  the server will receive the name from the client
        name = client_socket.recv(1024).decode('utf-8')
        client_socket.send("Hello, {}!".format(name).encode('utf-8'))

        while True:
            #the server will receive the request from the client
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break

            print(f"Received request: {request} , from {client_socket.getpeername()}") # to print the info

            #the server will process the request and send the response back to the client
            if request == "get_users":
                response1 = {"status_code": 200, "results": [] ,"message": "Success"}  #the server will send the response back to the client
                response = requests.get(f"https://api.groupme.com/v3/groups/{GROUP_ID}/members?token={API_KEY}") #the server will send the request to the server
                response1["results"] = response.json()["response"]["members"] #the response send to the client 
                client_socket.sendall(json.dumps(response1).encode('utf-8'))
    except Exception as e:
        print(f"Error handling request {client_address}: {e}")
        response_json = response.json() #the server will send the response back to the client
        client_socket.sendall(json.dumps(response_json).encode('utf-8'))
    finally:
        client_socket.close()
        print(f"Connection closed with {client_socket.getpeername()}")




#to can integrate with the start _server function
def main ():
    "the main function will start the server and handle incoming connections"
    server_socket = start_server()
    try:
      while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
    except KeyboardInterrupt:
        print("Server stopped... Goodbye!")
        server_socket.close()
    except Exception as e :
        print(f"Error: {e}")
    finally:
        server_socket.close()

        #to run the server in the main function 
        if __name__ == "__main__":
            main()
