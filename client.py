import socket
import json

def enumerate_list(options):
    #number options-to avoid redundancy
    for index, option in enumerate(options, start=1): 
        print(f"{index}- {option}")

def req_to_server(client_s,req):
    enc_req=json.dump(req).encode("utf-8")
    client_s.sendall(enc_req) #instead of sendto, this is for tcp


def router(option):
    match option:
        case 1:
            handle_headlines()
        case 2:
            handle_sources()
        case 3:
            handle_quit()

def handle_headlines(client_s):
    menu=["Search for Keywords", "Search by Category", "Search by Country", "List all new headlines", "Back to main menu"]
    print("=== Headlines Menu ===")
    action=int(input(enumerate_list(menu)))
    match action:
        case 1:
            parameter=input("Enter Keyword: ")
        case 2:
            categories=["Business", "General", "Health", "Science", "Sports", "Technology"]
            print("=== Categories ===")
            enumerate_list(categories)
            parameter=input("Select Category: ")
        case 3:
            countries=["AU", "CA", "JP", "AE", "SA", "KR", "US", "MA"] #use casefold incase the user inputs country in dif case
            print("=== Countries ===")
            enumerate_list(countries)
            parameter=input("Search by country")
        case 4:
            parameter="List all new headlines"
        case 5:
            return                
    req={"option": "search_headlines" , "action": action , "parameter": parameter} #formulate req that will specify what headline is required
    req_to_server(client_s,req)



    
def handle_sources():
    menu=["Search by Category", "Search by Country", "Search by Language", "List all", "Back to main menu"]

def handle_quit():


def main():
    server_add=("localhost", 8080)
    client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP socket connection
    client_s.connect(server_add) #connect to server
    print("You've successfully connected to the server {}".format(server_add)) #successful msg
    search=["Search headlines", "List of sources", "Quit"]
    username = input("Welcome, please type your name:\n")
    print(f"Hello {username}, choose a number: ")
    print("===Main Menu===\n")
    enumerate_list(search)
    action = int(input("Select an option: "))
    router(action)



    








if __name__ == "__main__":
    main()

    