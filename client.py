import socket
import json

def enumerate_list(options):
    #this will number the options manually
    for index, option in enumerate(options, start=1): 
        print(f"{index}- {option}")

def router(option):
    match option:
        case (1):
            handle_headlines()
        case(2):
            handle_sources()
        case (3):
            handle_quit()

def handle_headlines():
    menu=["Search for Keywords", "Search by Category", "Search by Country", "List all new headlines", "Back to main menu"]
    
def handle_sources():

def handle_quit():


def main():
    search=["Search headlines", "List of sources", "Quit"]
    username = input("Welcome to this humble News Server. Please type your name:\n")
    print(f"Hello {username}, please choose a number: ")
    print("===Main Menu===\n")
    enumerate_list(search)
    action = int(input("Select an option: "))
    router(action)

    








if __name__ == "__main__":
    main()

    