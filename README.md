
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


