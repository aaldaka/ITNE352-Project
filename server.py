import socket
import threading
import pickle
import requests
import json
import os

# Constants
API_KEY = "130a3a3c32144eaa95bab0c44d5668ae"
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8081
HEADLINES_URL = "https://newsapi.org/v2/top-headlines"
SOURCES_URL = "https://newsapi.org/v2/sources"
GROUP_ID = "A11"  

# make sure the save directory exists
SAVE_DIR = "saved_requests"
os.makedirs(SAVE_DIR, exist_ok=True)

def start_server():
    """Start the server and listen for incoming connections.."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(7) # allow up to 7 concurrent connections
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")
    return server_socket

def handle_client(client_socket, client_address):
    """Handle the connection for a single client..."""
    print(f"Accepted connection from {client_address}")
    # Receive the request data from the client using pickle (deserialization)
    try: 
        while True: # keep the connection open until the client disconnects
            request_data = client_socket.recv(4096)
            if not request_data:
                break

            try:
                # Parse the request as a pickle object
                request = pickle.loads(request_data)

                # take  the username from the request and print it
                username = request.get("username", "Unknown")
                print(f"Request received from user: {username}")

                # Process the request based on its type 
                response = process_request(request, username)
                client_socket.sendall(pickle.dumps(response))
            except Exception as e:
                error_message = {
                    "status_code": 400,
                    "message": "Error processing request",
                    "error": str(e)
                }
                client_socket.sendall(pickle.dumps(error_message))
                print(f"Error handling request: {e}")
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"Connection closed with {client_address}")


def process_request(request, client_name):
    """Process the client's request and return the appropriate response..."""
    print(f"Processing request: {request}")
    request_type = request.get("type")
    action = request.get("action")
    param = request.get("parameter")

    if request_type == "headlines":
        return fetch_data(action, param, client_name, "headlines")
    elif request_type == "sources":
        return fetch_data(action, param, client_name, "sources")
    else:
        return {"status_code": 400, "message": "Invalid request type"}

def fetch_data(action, param, client_name, request_type):
    """Fetch data from NewsAPI based on the request type... """
    url = HEADLINES_URL if request_type == "headlines" else SOURCES_URL
    params = {"apiKey": API_KEY}

    if request_type == "headlines":
        params["pageSize"] = 15

        if action == 0:  # Search by keyword
            params["q"] = param
        elif action == 1:  # Search by category
            params["category"] = param.lower()
        elif action == 2:  # Search by country
            params["country"] = param.lower()
        elif action == 3:
            params["country"] = "us"    
    elif request_type == "sources":
        if action == 0:  # Search by category
            params["category"] = param.lower()
        elif action == 1:  # Search by country
            params["country"] = param.lower()
        elif action == 2:  # Search by language
            params["language"] = param.lower()

    try: # use a timeout of 10 seconds for the request to avoid hanging the server if the API is down or slow to respond 
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Format the results for the client and save it to a file if the user wants to save it
        if request_type == "headlines":
            articles = data.get("articles", [])
            
            if not articles:
                # No articles found for the provided parameters
                return {"status_code": 404, "message": "No articles found for the given parameters."}
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

        elif request_type == "sources":  # Fetch sources data from NewsAPI and format the results for the client and save it to a file if the user wants to save it
            sources = data.get("sources", [])
            if not sources:
                print("[WARNING] No sources found.")
                return {"status_code": 404, "message": "No sources found."}
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

        save_to_file(client_name, request_type, results)

        return {"status_code": 200, "type": request_type, "results": results}
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] API request failed: {e}")
        return {"status_code": 500, "message": "API request failed", "error": str(e)}
    except Exception as e:
        print(f"[ERROR] Failed to fetch {request_type}: {e}")
        return {"status_code": 500, "message": f"Failed to fetch {request_type}"}

def save_to_file(client_name, request_type, results):
    """Save the data to a JSON file for debugging purposes..."""
    file_name = f"{client_name}{request_type}{GROUP_ID}.json"
    file_path = os.path.join(SAVE_DIR, file_name)
    
    # Create the directory if it doesn't exist and ignore the error if it already exists (FileExistsError)
    try: 
        with open(file_path, "w") as json_file:
            json.dump(results, json_file, indent=4)
        print(f"Data saved to {file_path}")
    except Exception as e:
        print(f"Error saving data to file: {e}")

def main():
    """Start the server and handle incoming connections..."""
    server_socket = start_server()

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_handler = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address)
            )
            client_handler.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()

if __name__ == "_main_":
    main()
