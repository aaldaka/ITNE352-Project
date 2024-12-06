import socket
import pickle
import customtkinter as ck
import tkinter as tk

MAIN_MENU = ["Search Headlines", "List of Sources", "Quit"]
COUNTRIES = ["AU", "CA", "JP", "AE", "SA", "KR", "US", "MA"]
LANGUAGES = ["AR", "EN"]
CATEGORIES = ["Business", "General", "Health", "Science", "Sports", "Technology"]
HSUBMENU = ["Search for Keywords", "Search by Category", "Search by Country", "List all", "Back to main menu"]
SSUBMENU = ["Search by Category", "Search by Country", "Search by Language", "List all", "Back to main menu"]
action_buttons = [] #to be cleared
req={} #to be formulatted
keyword = ""
BUFFER_SIZE = 5000

app = ck.CTk()
app.title("ITNE352-News Server")
ck.set_appearance_mode("system")
ck.set_default_color_theme("blue")
app.geometry("450x550")


username_label = ck.CTkLabel(app, text="Hello\nEnter your name:")
username_label.pack(pady=10)
username_input = ck.CTkEntry(app)
username_input.pack(pady=10)

output_text = ck.CTkTextbox(app, width=500, height=200)
output_text.pack(pady=10)

def welcome():
    username = username_input.get().strip()
    if username:
        output_text.insert("end", f"Welcome, {username}!\nEnjoy your ride throughout the news.\n")
        username_input.delete(0, 'end')
        username_label.pack_forget()  # Hide the username label
        username_input.pack_forget()   # Hide the input field
        button.place_forget()           # Hide the submit button
        handle_main()                  # Show main menu
    else:
        output_text.insert("end", "Please enter a valid name.\n")


def handle_main():
    clearingButtons()
    output_text.insert("end", "=== Select a main menu button option ===\n")

    for item in MAIN_MENU:
        button = ck.CTkButton(app, text=item, command=lambda item=item: router(item))
        button.pack(pady=5)
        action_buttons.append(button)


def router(action):
    clearingButtons()
    if action == "Search Headlines":
        handle_headlines()
    elif action == "List of Sources":
        handle_sources()
    elif action == "Quit":
        app.quit()        

def handle_req(type, action, parameter):  # Formats data using pickle, to send to the server
    request_data = {
        "type": type,  # Type of request: headlines, sources, etc.
        "action": action,  # Action: e.g., search by keyword, category, country
        "parameter": parameter  # The actual parameter (e.g., keyword, category, etc.)
    }

    # Serialize the request data using pickle
    encoded_request = pickle.dumps(request_data)

    # Create a socket and send the request to the server
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_s:
            client_s.connect(("127.0.0.1", 8081))  # Connect to the server (adjust IP and port as needed)
            client_s.sendall(encoded_request)  # Send the encoded request

            # Receive the response from the server
            response_data = b""  # Ensure this is binary
            while True:
                part = client_s.recv(1024)  # Assuming 1024 byte buffer size
                response_data += part
                if len(part) < 1024:
                    break

            # Deserialize the response
            response = pickle.loads(response_data)

            # Handle the response (based on the type and action)
            if response.get("status_code") == 200:
                output_text.insert("end", f"Results for {parameter}:\n")
                display_results(response)
            else:
                output_text.insert("end", f"Error: {response.get('message', 'Unknown error occurred')}\n")
    except Exception as e:
        output_text.insert("end", f"Error communicating with server: {e}\n")

def handle_res(client_s):
    # Receive the response from the server
    try:
        response_data = b""  # Initialize empty byte string to store response
        while True:
            part = client_s.recv(BUFFER_SIZE)  # Receive response in chunks
            response_data += part
            if len(part) < BUFFER_SIZE:
                break

        if not response_data:
            output_text.insert("end", "No data received from server.\n")
            return

        response = pickle.loads(response_data)  # Decode the byte data to a Python object

        # Handle the response based on the status code
        if response.get("status_code") == 200:
            output_text.insert("end", f"Results for {response['parameter']}:\n")
            display_results(response)  # Display the results in the GUI
        else:
            output_text.insert("end", f"Error: {response.get('message', 'Unknown error occurred')}\n")

    except Exception as e:
        output_text.insert("end", f"Error decoding response from server: {e}\n")


def display_results(response):
    results = response.get("results", [])[:15]  # Limit to first 15 results
    if not results:
        output_text.insert("end", "No results found.\n")
        return

    # Clear the current contents of the output_text
    output_text.insert("end", "\n=== Results ===\n")

    # Create buttons for each result in the list
    for i, res in enumerate(results):
        if response["type"] == "headlines":
            result_text = f"{i}. {res['source_name']}: {res['author']} presents {res['title']}"
        elif response["type"] == "sources":
            result_text = f"{i}. {res['source_name']}"

        # Display result text in the output_text
        output_text.insert("end", result_text + "\n")

        # Create a button for each result that triggers the display_details function
        button = ck.CTkButton(app, text=f"View {i}", command=lambda idx=i: display_details(response["type"], results[idx]))
        button.pack(pady=5)

    # Add a back button to go back to the headlines menu or main menu
    back_button = ck.CTkButton(app, text="Back", command=handle_main)
    back_button.pack(pady=5)

def display_details(result_type, result):
    output_text.insert("end", "\n=== Details ===\n")
    
    if result_type == "headlines":
        output_text.insert("end", f"Title: {result['title']}\n")
        output_text.insert("end", f"Source: {result['source_name']}\n")
        output_text.insert("end", f"Author: {result['author']}\n")
        output_text.insert("end", f"Published: {result['publish_date']}\n")
        output_text.insert("end", f"URL: {result['url']}\n")

    elif result_type == "sources":
        output_text.insert("end", f"Source Name: {result['source_name']}\n")

    back_button = ck.CTkButton(app, text="Back to Results", command=lambda: display_results(result))
    back_button.pack(pady=5)

#--------------------------Headline handling-------------------
def handle_headlines():
    clearingButtons()

    output_text.insert("end", "\n=== Select a headline menu button option ===\n")
    for index, item in enumerate(HSUBMENU):
        button = ck.CTkButton(app, text=item, command=lambda index=index: handle_headline_action(index))
        button.pack(pady=5)
        action_buttons.append(button)


def handle_headline_action(action):
    clearingButtons()

    if action == 0:  # Search by Keyword
        user_inp("Enter Keyword:", process_headline_input, action)
    elif action == 1:  # Search by Category
        handle_category_selection("headlines")
    elif action == 2:  # Search by Country
        handle_country_selection("headlines")
    elif action == 3:  # List all
        handle_req("headlines", action, "List all")
        handle_main()  # Return to the main menu
    elif action == 4:  # Back to main menu
        handle_main()
      
def handle_category_selection(type):
    clearingButtons()

    output_text.insert("end", "\n=== Categories ===\n")
    for index, category in enumerate(CATEGORIES):
        button = ck.CTkButton(app, text=category, command=lambda index=index, type=type: category_selected(index,type))
        button.pack(pady=5)
        action_buttons.append(button)
    
    # Add back button
    back_button = ck.CTkButton(app, text="Back to Headlines", command=handle_headlines)
    back_button.pack(pady=5)
    action_buttons.append(back_button)

def category_selected(index,type):
    parameter = CATEGORIES[index]
    handle_req(type,1,parameter)
    handle_main()  # Go back to main menu after handling

def handle_country_selection(type):
    clearingButtons()

    output_text.insert("end", "\n=== Countries ===\n")
    for index, country in enumerate(COUNTRIES):
        button = ck.CTkButton(app, text=country, command=lambda index=index, type=type: country_selected(index,type))
        button.pack(pady=5)
        action_buttons.append(button)

    # Add back button
    back_button = ck.CTkButton(app, text="Back to Headlines", command=handle_headlines)
    back_button.pack(pady=5)

button = ck.CTkButton(master=app, text="Submit", command=welcome)
button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def country_selected(index,type):
    parameter = COUNTRIES[index]
    handle_req(type,1,parameter)
    handle_main()

def user_inp(prompt, callback, action):
    action_buttons.clear()
    # Create a frame to contain the prompt, input bar, and submit button
    input_frame = ck.CTkFrame(app)
    input_frame.pack(pady=10)

    # Display the prompt above the input bar
    prompt_label = ck.CTkLabel(input_frame, text=prompt, anchor="w")
    prompt_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)

    # Input bar (Entry widget)
    input_bar = ck.CTkEntry(input_frame, width=200, placeholder_text="Type here...")
    input_bar.grid(row=1, column=0, padx=5)

    # Function to handle submit action
    def submit_action():
        user_input = input_bar.get().strip()  # Retrieve user input
        if user_input:  # If input is valid
            callback(user_input, action)  # Send the input back to the provided callback
        else:
            # Display a warning if input is empty
            error_label = ck.CTkLabel(input_frame, text="Input cannot be empty!", fg_color="red")
            error_label.grid(row=2, column=0, columnspan=2)
        input_frame.forget()    

    # Submit button to confirm input
    submit_button = ck.CTkButton(input_frame, text="Submit", command=submit_action)
    submit_button.grid(row=1, column=1, padx=5)

def process_headline_input(input_keyword, action):
    keyword = input_keyword.strip()  # Store the entered keyword
    if keyword:  # Ensure the keyword is not empty
        handle_req("headlines", action, keyword)  # Use handle_req to send the request
        handle_main()  # Return to the main menu after handling the input
    else:
        output_text.insert("end", "Keyword cannot be empty!\n")

#-----------------------Sources-----------------
def handle_sources():
    output_text.insert("end", "\n=== Sources Menu ===\n")
    for index, item in enumerate(SSUBMENU):
        button = ck.CTkButton(app, text=item, command=lambda index=index: handle_source_action(index))
        button.pack(pady=5)
        action_buttons.append(button)

def handle_source_action(action):
    clearingButtons()

    if action == 0:  # Search by Category
        handle_category_selection("sources")
    elif action == 1:  # Search by Country
        handle_country_selection("sources")
    elif action == 2:  # Search by language
        handle_language_selection()
    elif action == 3:  # List all
        handle_req("sources", action, "List all")
        handle_main()  # Return to the main menu
    elif action == 4:  # Back to main menu
        handle_main()

def handle_language_selection():
    for button in action_buttons:
        button.pack_forget() 
    output_text.insert("end", "\n=== Languages ===\n")
    for index, language in enumerate(LANGUAGES):
        button = ck.CTkButton(app, text=language, command=lambda index=index, type=type: language_selected(index))
        button.pack(pady=5)
        action_buttons.append(button)

    # Add back button
    back_button = ck.CTkButton(app, text="Back to Sources", command=handle_sources)
    back_button.pack(pady=5)

def language_selected(index):
    parameter = LANGUAGES[index]
    handle_req("sources", 2, parameter)
    handle_main()

def clearingButtons():
    for button in action_buttons:
        button.pack_forget()
    action_buttons.clear()

app.mainloop()