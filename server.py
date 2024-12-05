import socket
import threading
import json
import requests

API_KEY = "130a3a3c32144eaa95bab0c44d5668ae"  # Your NewsAPI key
GROUP_ID = "group_A11"  # Group identifier
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080

def start_server():
    """Start the server and listen for incoming connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)  # Allow up to 5 simultaneous connections
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")
    return server_socket

def handle_client(client_socket, client_address):
    """Handle the connection for a single client."""
    print(f"Accepted connection from {client_address}")
    try:
        # Receive the client's name
        name = client_socket.recv(1024).decode('utf-8')
        client_socket.send(f"Hello, {name}!".encode('utf-8'))

        while True:
            # Receive a request from the client
            request_data = client_socket.recv(1024).decode('utf-8')
            if not request_data:
                break

            print(f"Received request: {request_data} from {client_address}")

            try:
                # Parse the request as JSON
                request = json.loads(request_data)

                # Process the request based on its type
                response = process_request(request, name)

                # Send the response to the client
                client_socket.sendall(json.dumps(response).encode('utf-8'))
            except json.JSONDecodeError:
                error_message = {"status_code": 400, "message": "Invalid JSON format"}
                client_socket.sendall(json.dumps(error_message).encode('utf-8'))
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"Connection closed with {client_address}")

def process_request(request, client_name):
    """Process the client's request and return the appropriate response."""
    request_type = request.get("type")
    action = request.get("action")
    param = request.get("param")

    if request_type == "headlines":
        return fetch_data(action, param, client_name, "headlines")
    elif request_type == "sources":
        return fetch_data(action, param, client_name, "sources")
    else:
        return {"status_code": 400, "message": "Invalid request type"}

def fetch_data(action, param, client_name, request_type):
    """Fetch data from NewsAPI based on the request type."""
    url = "https://newsapi.org/v2/top-headlines" if request_type == "headlines" else "https://newsapi.org/v2/top-headlines/sources"
    params = {"apiKey": API_KEY}

    if request_type == "headlines":
        params["pageSize"] = 15
        params["language"] = "en"
        if action == 0:  # Search by keyword
            params["q"] = param
        elif action == 1:  # Search by category
            params["category"] = param.lower()
        elif action == 2:  # Search by country
            params["country"] = param.lower()
    elif request_type == "sources":
        if action == 0:  # Search by category
            params["category"] = param.lower()
        elif action == 1:  # Search by country
            params["country"] = param.lower()
        elif action == 2:  # Search by language
            params["language"] = param.lower()

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Save data to a JSON file for debugging
        save_data(data, client_name, request_type)

        # Format the results for the client
        if request_type == "headlines":
            articles = data.get("articles", [])
            results = [
                {
                    "source_name": article["source"]["name"],
                    "author": article.get("author", "Unknown"),
                    "title": article["title"],
                    "url": article["url"],
                    "description": article.get("description", "No description available"),
                    "publish_date": article["publishedAt"].split("T")[0],
                    "publish_time": article["publishedAt"].split("T")[1].split("Z")[0],
                }
                for article in articles[:15]
            ]
        elif request_type == "sources":
            sources = data.get("sources", [])
            results = [
                {
                    "source_name": source["name"],
                    "description": source["description"],
                    "url": source["url"],
                    "category": source["category"],
                    "language": source["language"],
                    "country": source["country"],
                }
                for source in sources[:15]
            ]
        return {"status_code": 200, "type": request_type, "results": results}
    except Exception as e:
        print(f"[ERROR] Failed to fetch {request_type}: {e}")
        return {"status_code": 500, "message": f"Failed to fetch {request_type}"}

def save_data(data, client_name, request_type):
    """Save the data to a JSON file for debugging purposes."""
    file_name = f"{client_name}_{request_type}_results.json"
    with open(file_name, "w") as file:
        json.dump(data, file)
    print(f"Data saved to {file_name}")

def main():
    """Start the server and handle incoming connections."""
    server_socket = start_server()
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServer stopped... Goodbye!")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
