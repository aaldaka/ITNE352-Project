import socket
import json

#global vars to avoid redundancy
COUNTRIES = ["AU", "CA", "JP", "AE", "SA", "KR", "US", "MA"]
LANGUAGES = ["AR", "EN"]
CATEGORIES = ["Business", "General", "Health", "Science", "Sports", "Technology"]
HSUBMENU = ["Search for Keywords", "Search by Category", "Search by Country", "List all New headlines", "Back to main menu"]
SSUBMENU = ["Search by Category", "Search by Country", "List all", "Back to main menu"]

def enumerate_list(options):#avoiding redundancy
    for index, option in enumerate(options, start=0): 
        print(f"{index}- {option}")

def handle_req(client_s,req):
    enc_req=json.dump(req).encode("utf-8")
    client_s.sendall(enc_req) #instead of sendto, this is for tcp

def handle_res(client_s):
    response = json.loads(client_s.recv(4096).decode('utf-8'))
    if response.status_code == 200: #success
        print("=== Results ===")
        display_results(response)
    else:
        print("Error: Unknown error occured") #could be more specific    
        
def display_results(response):
    results=response.get("results", [])[:15]
    if not results: #it was an empty slice
     print("No results found")
     return
    
    for i, res in enumerate(results, start=0):
        if response["type"]=="headlines": #src, auth, title
            print(f"{i}- {res["source_name"]}: {res["author"]} presents {res["title"]}")
        elif response["type"]=="sources":
            print(f"{i}- {res["source_name"]}")    
        option=int(input("Select a number to view further details, else -1 to return:\n "))

        if option==-1:
            return
        elif 0<= option <len(results):
            display_details(response["type"], results[option])
        else:
            print("Invalid option")    
            return
        
def display_details(res_type, res):
    if res_type=="headlines":
        print("\n=== Headline Details ===")
        print(f"Source: {res_type["source_name"]}")
        print(f"Author: {res_type["author"]}")
        print(f"Title: {res_type["title"]}")
        print(f"URL: {res_type["url"]}")
        print(f"Description: {res_type["description"]}")
        print(f"Published Date: {res_type["publish_date"]}")
        print(f"Published Time: {res_type["publish_time"]}")
    elif res_type=="sources":
        print("\n=== Source Details ===")            
        print(f"Source: {res_type["source_name"]}")
        print(f"Country: {res_type["country"]}")
        print(f"Description: {res_type["description"]}")
        print(f"URL: {res_type["url"]}")
        print(f"Category: {res_type["category"]}")
        print(f"Language: {res_type["language"]}")

def router(client_s):
    while True:
        main_menu=["Search Headlines", "List of Sources", "Quit"]
        print("===Main Menu===\n")
        enumerate_list(main_menu)
        action = int(input("Select an option: "))
        match action:
            case 1:
                handle_headlines(client_s)
            case 2:
                handle_sources(client_s)
            case 3:
                print("Exiting the program, goodbye!")
                handle_quit(client_s)

def handle_headlines(client_s):  
    print("=== Headlines Menu ===")
    action = int(input(enumerate_list(HSUBMENU)))
    
    if 0 <= action <= 4:
        if action == 0: #Keyword
            parameter = input("Enter Keyword: ")
        elif action == 1:  #Category
            print("=== Categories ===")
            choice = int(input(enumerate_list(CATEGORIES)))
            parameter = CATEGORIES[choice]
        elif action == 2:  #Country
            print("=== Countries ===")
            choice = int(input(enumerate_list(COUNTRIES)))
            parameter = COUNTRIES[choice]
        elif action == 3: 
            parameter = "List all"
        elif action == 4: 
            router(client_s)
            return
    else:
        print("Invalid option!")  # Handle invalid input
        return

    req = {"type": "headlines", "action": action, "parameter": parameter}
    handle_req(client_s, req)


def handle_sources(client_s): #need to map actions to proper actions
    print("=== Sources Menu ===")
    action=int(input(enumerate_list(SSUBMENU)))
    
    # is action choice allowed?
    if 0<= action <4:
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
    req={"type": "sources" , "action": action , "parameter": parameter} #formulate req that will specify what headline is required
    handle_req(client_s,req)

def handle_quit(client_s):
    print("Thank you for your time, goodbye!")
    client_s.close()
    exit()

def main():
    server_add=("localhost", 8080)
    client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP socket connection
    client_s.connect(server_add) #connect to server
    print(f"You've successfully connected to the server {server_add}") #successful msg
    username = input("Welcome, please type your name:\n")
    print(f"Welcome {username}, choose an option: ")
    router(client_s)




    








if __name__ == "__main__":
    main()

    