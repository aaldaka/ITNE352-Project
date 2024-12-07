
# Multithreaded News Client/Server Information System NewsBeacon

This is a python oriented project that provides real-time news updates from various sources that allows to navigate through headlines, view articles and explore a wide range of categories.

## Semester
- *S1 2024-2025*
## Group
- **A11**
- **ITNE352**
- Section: **1**

**Authors/Students**
- Alya Hasan Abdulla - 202208622
- Maryam Ali Hasan   - 202209427


## Table of Contents
    1. Requirements
    2. How to run the system
    3. Explanation of client.py 
    4. Explanation of server.py 
    5. Additional concept
    6. Acknowledgments
    7. Conclusion


## Requirements
### Prerequisites 
- Given this is a python proj, you must have python downloaded in your system -> https://www.python.org/downloads/.
- API Key, this will allow you to utilise the NewsAPI. 

#### Installation and Dependancies 
- Cloning the repositry is the first step -> https://github.com/aaldaka/ITNE352-Project-A11.git 
- Then you must install several modules using "pip install ...", these modules include: customtkinter(Enhanced UI with widgets) and requests(Making HTTP requests to the NewsAPI).
- In server.py, set your API key for the news service.



## How to run
- In the terminal, type the command "python server.py" to firstly run the server.
- Next, your run the client's GUI by typing "python client.py".
- In the end the GUI will prompt you to choose several options for your news requests.
## Client script
The client script is responsible for displaying the results and navigating through the options via GUI.

### Imports:
Here are the imported packages for this script:
```python
import socket # Interactions between client and server
import pickle # Used for de/serialization (better data transfter) 
import customtkinter as ck # Customization
import tkinter as tk # Customization
import threading # Additional to deload processes
```
### Functions
### Variables: 
These were initialized to clean up the functions
```python
MAIN_MENU = ["Search Headlines", "List of Sources", "Quit"]
COUNTRIES = ["AU", "CA", "JP", "AE", "SA", "KR", "US", "MA"]
LANGUAGES = ["AR", "EN"]
CATEGORIES = ["Business", "General", "Health", "Science", "Sports", "Technology"]
HSUBMENU = ["Search for Keywords", "Search by Category", "Search by Country", "List all", "Back to main menu"]
SSUBMENU = ["Search by Category", "Search by Country", "Search by Language", "List all", "Back to main menu"]
action_buttons = [] # to be cleared
dynamic_widgets = []
req = {} # to be formulatted
keyword = ""
BUFFER_SIZE = 4075
clientName = ""
```

- **welcome()** uses a window widget that was created using ck to greet the client and store its name.
```python
def welcome(): # Welcoming user
    global clientName
    username = username_input.get().strip()
    if username:
        clientName=username
        output_text.insert("end", f"Welcome, {clientName}!\nEnjoy your ride throughout the news.\n")
        username_input.delete(0, 'end')
        username_label.pack_forget()  # Hides the previous inputs and labels
        username_input.pack_forget()   
        button.place_forget()       
        app.after(2000, handle_main)  # Pause before redirection
    else:
        output_text.insert("end", "Please enter a valid name.\n")

button = ck.CTkButton(master=app, text="Submit", command=welcome)
button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
```
- These functions deal with displaying main menu, and the redirections to other menus.
```python
def handle_main(): # Displays main menu
    clearingButtons()
    output_text.delete("1.0", "end")  # Clear previous output
    output_text.insert("end", "Select a main menu button option\n")

    for item in MAIN_MENU:
        button = ck.CTkButton(app, text=item, command=lambda item=item: router(item))
        button.pack(pady=5)
        action_buttons.append(button)

def router(action): # Redirections to menus
    clearingButtons()
    if action == "Search Headlines":
        handle_headlines()
    elif action == "List of Sources":
        handle_sources()
    elif action == "Quit":
        app.quit()    
```        
- These functions (Too long to show here) deal with both headlines and sources results and details, it modifies the displayed info based on the type.
```python
# Handles Results and Details
def display_results(response):
def display_details(result_type, result,response):    
```

- These functions capture the client's option, and then sends it to the action handlers.
- **handle_headline_action(action)** has an option "Search by Keyword", in addition to that helper functions **user_inp(), submit_action()** to capture the keyword and **process_headline_input()** to formulate the request with it.

```python
def handle_headlines()
def handle_sources()

def handle_headline_action(action):
def handle_source_action(action):
```
- Helper functions that will reduce redundancy.
```python
def clearingButtons(): # Clears buttons and widgets in action_buttons and dynamic_widgets
def dynamicBack(type): # Creates a back button to either headlines or sources menus
```

## Server Script

The "server.py" handles all the requirements coming from the client, through this it takes the news data from the NewsAPI, then it can resend the necessary response to the client again. It was designed to be able to manage communication between many clients at the same time.

### Imports 
```python
import socket #Allows for network connection from client or server interaction
import threading #Supports multiple management of more than one client requested 
import pickle #Convert Python data structures into format to make the transmit easier 
import requests #Simplifies sending the request 
import json #Manages the processing of JSON data 
import os # Communicates with the os for file and directory 
 ```

### Constants 
- API_KEY = "130a3a3c32144eaa95bab0c44d5668ae"
- SERVER_HOST = "127.0.0.1"
- SERVER_PORT = 8081
- HEADLINES_URL = "https://newsapi.org/v2/top-headlines"
- SOURCES_URL = "https://newsapi.org/v2/sources"
- GROUP_ID = "A11"  

### make the Directory Setup
To make sure the right directory for saving the results exist. 
```python
SAVE_DIR = "saved_requests"
os.makedirs(SAVE_DIR, exist_ok=True)
```
### Server functions 
#### start_server()
At first , start the server to make sure that it can listen for the upcoming connections from clients for the specific host and port number.

```python
def start_server():
    """Start the server and listen for incoming connections.."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(7) # allow up to 7 concurrent connections
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")
    return server_socket
    ```

#### handle_client(client_socket, client_address)
Holds the communication with the client, to get the request send the response back.

```python
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
```

#### process_request(request, client_name)
Make a procedure with the client request thats found in the type (whether it is headlines or sources) so then that calls the fetch_data function to extract the important info from it.

```python
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
```

#### fetch_data(action, param, client_name, request_type)
This gets the data from the NewsAPI that is related to the client's request, then construct the right response format.

```python
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
                print("[WARNING] No articles found for the given keyword. Trying default request.")
                params = {"apiKey": API_KEY, "country": "us", "pageSize": 15, "language": "en"}
                response = requests.get(HEADLINES_URL, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
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
            if not results:
                return {"status_code": 404, "message": "No articles found for the keyword."}

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
```

#### save_to_file(client_name, request_type, results)
This saves the result and appends them as JSON files in **saved_requests** directory.

```python
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
```

#### The Main function
This starts the server and makes sure it accepts the upcoming client connection for the request, then it creates a new thread related to each client.
```python
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

if __name__ == "__main__":
    main()

```

### Additional Concepts
- Implement the GUI using tkinter and customtkinter.

### Acknowledgments
We'd like to thank:

- Dr. Mohamed A. Almeer for his lead and help during this project.
- Our teammates for their hard work and collaboration.

### Conclusion 
In this project we explored a new programming language **Python** and challenged our obtained knowledge in creating a client/server news system. We have faced many difficulties and obstacles especially after implementing the GUI, but in the end with some research we were able to resolve our own doubts. We learned a lot of new concepts like using pickle, tkinter and threading. This was an exceptional journey to take part of.

### Resources
- Socket Programming in Python : https://realpython.com/python-sockets/
- NewsAPI: https://newsapi.org/
- Threading in Python : https://docs.python.org/3/library/threading.html
- tkinter : https://www.bing.com/ck/a?!&&p=1a12c8d7634ee4a94678fd1b455ad38da2ec4047e62720d295009b70f9100135JmltdHM9MTczMzUyOTYwMA&ptn=3&ver=2&hsh=4&fclid=08e4a44d-3045-67d7-2583-b679314c66a2&psq=kinter+document&u=a1aHR0cHM6Ly9kb2NzLnB5dGhvbi5vcmcvMy9saWJyYXJ5L3RraW50ZXIuaHRtbA&ntb=1


