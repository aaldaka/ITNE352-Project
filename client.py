import socket
import json

#global vars to avoid redundancy
COUNTRIES = ["AU", "CA", "JP", "AE", "SA", "KR", "US", "MA"]
LANGUAGES = ["AR", "EN"]
CATEGORIES = ["Business", "General", "Health", "Science", "Sports", "Technology"]
HSUBMENU = ["Search for Keywords", "Search by Category", "Search by Country", "List all New headlines", "Back to main menu"]
SSUBMENU = ["Search by Category", "Search by Country", "List all", "Back to main menu"]

def enumerate_list(options):
    #number options-to avoid redundancy
    for index, option in enumerate(options, start=0): 
        print(f"{index}- {option}")

# def formulate_req()
def req_to_server(client_s,req):
    enc_req=json.dump(req).encode("utf-8")
    client_s.sendall(enc_req) #instead of sendto, this is for tcp


def router(client_s):
    while True:
        main_menu=["Search headlines", "List of sources", "Quit"]
        print("===Main Menu===\n")
        enumerate_list(main_menu)
        action = int(input("Select an option: "))
        match action:
            case 1:
                handle_headlines(client_s)
            case 2:
                handle_sources(client_s)
            case 3:
                print("Exiting the program")
                handle_quit(client_s)

def handle_headlines(client_s): #fix this make it similar to sources
    print("=== Headlines Menu ===")
    action=int(input(enumerate_list(SUBMENU)))
    match action:
        case 1:
            parameter=input("Enter Keyword: ")
        case 2:
            print("=== Categories ===")
            parameter=int(input(enumerate_list(CATEGORIES)))
        case 3:
            print("=== Countries ===")
            parameter=int(input(enumerate_list(COUNTRIES)))
        case 4:
            parameter="List all new headlines"
        case 5:
            router(client_s)
        case _:
            print("Invalid option")                 
    req={"option": "search_headlines" , "action": action , "parameter": parameter} #formulate req that will specify what headline is required
    req_to_server(client_s,req)

def handle_sources(client_s): #need to map actions to proper actions
    print("=== Sources Menu ===")
    action=int(input(enumerate_list(SSUBMENU)))
    
    # is action choice allowed?
    if 0 <= action < 4:
        if action == 0:
            print("=== Categories ===")
            category_choice = int(input(enumerate_list(CATEGORIES))) 
            parameter = CATEGORIES[category_choice]
        elif action == 1: 
            print("=== Countries ===")
            country_choice = int(input(enumerate_list(COUNTRIES)))
            parameter = COUNTRIES[country_choice]
        elif action == 2:
            parameter = "List all"
        elif action == 3: 
            router(client_s)
            return 
    else:
        print("Invalid option!") 
        return 
    req={"option": "search_sources" , "action": action , "parameter": parameter} #formulate req that will specify what headline is required
    req_to_server(client_s,req)

def handle_quit(client_s):
    print("Thank you for your time, goodbye!")
    client_s.close()
    exit()

def main():
    server_add=("localhost", 8080)
    client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP socket connection
    client_s.connect(server_add) #connect to server
    print(f"You've successfully connected to the server {server_add}") #successful msg
    # search=["Search headlines", "List of sources", "Quit"]
    username = input("Welcome, please type your name:\n")
    print(f"Welcome {username}, choose an option: ")
    router(client_s)




    








if __name__ == "__main__":
    main()

    