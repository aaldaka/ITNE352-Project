import socket
import pickle

# Global vars
COUNTRIES = ["AU", "CA", "JP", "AE", "SA", "KR", "US", "MA"]
LANGUAGES = ["AR", "EN"]
CATEGORIES = ["Business", "General", "Health", "Science", "Sports", "Technology"]
HSUBMENU = ["Search for Keywords", "Search by Category", "Search by Country", "List all News headlines", "Back to main menu"]
SSUBMENU = ["Search by Category", "Search by Country", "Search by Language", "List all", "Back to main menu"]

BUFFER_SIZE = 4096  # Adjust buffer size if needed

def enumerate_list(options):
    for index, option in enumerate(options):
        print(f"{index}- {option}")
    return "\nSelect an option: "

def handle_quit(client_s):
    print("Thank you for your time, goodbye!")
    client_s.close()
    exit()

def router(client_s): #Midpoint that handles the client's reqs
    while True:
        main_menu = ["Search Headlines", "List of Sources", "Quit"]
        print("\n=== Main Menu ===")
        enumerate_list(main_menu)
        try:
            action = int(input("Select an option: "))
            if action == 0:
                handle_headlines(client_s)
            elif action == 1:
                handle_sources(client_s)
            elif action == 2:
                print("Exiting the program...")
                handle_quit(client_s)
            else:
                print("Invalid option! Please try again.")
        except ValueError:
            print("Please enter a valid number.")


def handle_req(client_s, req): #Sends client's req
    try:
        encode_req = pickle.dumps(req) #Helps encode complex data to transfer better
        client_s.sendall(encode_req)
    except Exception as e:
        print(f"Error sending request: {e}")

def handle_res(client_s):#Recv the rec from the server
    try:
        response_data = b""
        while True: #Appends responses byte by byte
            part = client_s.recv(BUFFER_SIZE)
            response_data += part
            if len(part) < BUFFER_SIZE:
                break

        if not response_data:
            print("No data received from server.")
            return

        response = pickle.loads(response_data) #Decoded
        if response.get("status_code") == 200: #No errors, display
            print("\n=== Results ===")
            display_results(response)
        else:
            print(f"Error: {response.get('message', 'Unknown error occurred')}") #Code not 200
    except Exception as e:
        print(f"Error decoding response from server: {e}") #Error rec/decoding handling

def handle_headlines(client_s):
    print("\n=== Headlines Menu ===")
    action = int(input(enumerate_list(HSUBMENU)))

    if 0 <= action <= 4:
        parameter = None
        if action == 0:  # Keyword
            parameter = input("Enter Keyword: ")
        elif action == 1:  # Category
            print("\n=== Categories ===")
            choice = int(input(enumerate_list(CATEGORIES)))
            parameter = CATEGORIES[choice]
        elif action == 2:  # Country
            print("\n=== Countries ===")
            choice = int(input(enumerate_list(COUNTRIES)))
            parameter = COUNTRIES[choice]
        elif action == 3:  # List all
            parameter = "List all"
        elif action == 4:  # Back to main menu
            return

        req = {"type": "headlines", "action": action, "parameter": parameter}
        handle_req(client_s, req)
        handle_res(client_s)
    else:
        print("Invalid option!")

def handle_sources(client_s):
    print("\n=== Sources Menu ===")
    action = int(input(enumerate_list(SSUBMENU)))

    if 0 <= action <= 4:
        parameter = None
        if action == 0:  # Category
            print("\n=== Categories ===")
            category_choice = int(input(enumerate_list(CATEGORIES)))
            parameter = CATEGORIES[category_choice]
        elif action == 1:  # Country
            print("\n=== Countries ===")
            country_choice = int(input(enumerate_list(COUNTRIES)))
            parameter = COUNTRIES[country_choice]
        elif action == 2:  # Language
            print("\n=== Languages ===")
            lang_choice = int(input(enumerate_list(LANGUAGES)))
            parameter = LANGUAGES[lang_choice]
        elif action == 3:  # List all
            parameter = "List all"
        elif action == 4:  # Back to main menu
            print("Going back to the main menu...")
            return

        req = {"type": "sources", "action": action, "parameter": parameter}
        handle_req(client_s, req)
        handle_res(client_s)
    else:
        print("Invalid option!")        

def display_results(response):
    results = response.get("results", [])[:15]
    if not results: #Empty/No res
        print("No results found.")
        return

    for i, res in enumerate(results):
        if response["type"] == "headlines":
            print(f"{i}- {res['source_name']}: {res['author']} presents {res['title']}")
        elif response["type"] == "sources":
            print(f"{i}- {res['source_name']}")

    try:
        option = int(input("Select a number to view further details, else -1 to return:\n"))
        if option == -1:
            return
        elif 0 <= option < len(results):
            display_details(response["type"], results[option])
        else:
            print("Invalid option.")
    except ValueError:
        print("Invalid input, returning to menu.")

def display_details(res_type, res):
    if res_type == "headlines":
        print("\n=== Headline Details ===")
        print(f"Source: {res['source_name']}")
        print(f"Author: {res['author']}")
        print(f"Title: {res['title']}")
        print(f"URL: {res['url']}")
        print(f"Description: {res['description']}")
        print(f"Published Date: {res['publish_date']}")
        print(f"Published Time: {res['publish_time']}")
    elif res_type == "sources":
        print("\n=== Source Details ===")
        print(f"Source: {res['source_name']}")
        print(f"Country: {res['country']}")
        print(f"Description: {res['description']}")
        print(f"URL: {res['url']}")
        print(f"Category: {res['category']}")
        print(f"Language: {res['language']}")

def main():
    client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_s.connect(("127.0.0.1", 8081))
    print(f"You've successfully connected to the server on port {8081}.")
    username = input("Welcome, please type your name:\n")
    client_s.send(username.encode('ascii'))
    print(f"Welcome {username}, choose an option: ")
    router(client_s)

if __name__ == "__main__":
    main()