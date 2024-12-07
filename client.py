import socket
import pickle
import customtkinter as ck
import tkinter as tk
import threading

#Variables
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

#Window
app = ck.CTk()
app.title("NewsBeacon")
ck.set_appearance_mode("system")
ck.set_default_color_theme("blue")
app.geometry("450x600")
global_font = ck.CTkFont(family = "Arial", size = 16, weight = "bold")

username_label = ck.CTkLabel(app, text="Hello\nEnter your name:")
username_label.pack(pady=10)
username_input = ck.CTkEntry(app)
username_input.pack(pady=10)
output_text = ck.CTkTextbox(app, width=500, height=200, font=global_font)
output_text.pack(pady=10)

def welcome(): # Welcoming user
    global clientName
    username = username_input.get().strip()
    if username:
        clientName=username
        output_text.insert("end", "────୨ৎ────\n")
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

def handle_main(): # Displays main menu
    clearingButtons()
    output_text.delete("1.0", "end")  # Clear previous output
    output_text.insert("end", "𑁍Select a main menu button option\n")

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

# Handles request
def handle_req(type, action, parameter):  # Formats data using pickle, to send to the server
    request_data = {
        "type": type,  # Type of request: headlines, sources, etc.
        "action": action,  # Action: e.g., search by keyword, category, country
        "parameter": parameter,  # The actual parameter (e.g., keyword, category, etc.)
        "username": clientName
    }
    print(request_data)
    encoded_request = pickle.dumps(request_data)
    threading.Thread(target=send_request_to_server, args=(encoded_request,)).start()  # Diff thread to handle the request

def send_request_to_server(encoded_request):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_s:
            print("Connecting to server...")
            client_s.connect(("127.0.0.1", 8081))  # Connect to the server
            print("Sending request...")
            client_s.sendall(encoded_request)  # Send the encoded request
            response_data = b"" 
            while True:
                part = client_s.recv(1024)
                response_data += part
                if len(part) < 1024:
                    break

            response = pickle.loads(response_data) # Deserialize the response
            app.after(0, process_response, response) # Update the GUI with the response in the main thread
    except Exception as e:
        app.after(0, output_text.insert, "end", f"Error communicating with server: {e}\n")
        print(f"Error: {e}")

def process_response(response):
    if response.get("status_code") == 200:
        clearingButtons()
        output_text.insert("end","Results\n")
        display_results(response)
    else:
        output_text.insert("end", f"Error: {response.get('message', 'Unknown error occurred')}\n")

# Handles Results and Details
def display_results(response):
    clearingButtons()
    output_text.delete("1.0", "end")  # Clear previous output
    results = response.get("results", [])[:15]  # Limit to first 15 results

    if not results:
        output_text.insert("end", "𑁍No results found.\nReturning to the main menu...\n")
        app.after(1500, handle_main)
        return  # Exit the function early
    
    output_text.insert("end", "𑁍Results\n")
    output_text.insert("end", "-Click on a record to view its details\n")

    # Create a frame to hold the Listbox and Scrollbar
    listbox_frame = ck.CTkFrame(app)
    listbox_frame.pack(pady=10, fill="both", expand=True)
    dynamic_widgets.append(listbox_frame)
    # Create a Listbox widget
    result_listbox = tk.Listbox(listbox_frame, height=15, selectmode=tk.SINGLE)
    result_listbox.pack(side="left", fill="both", expand=True)
    # Attach a scrollbar to the Listbox
    scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=result_listbox.yview)
    scrollbar.pack(side="right", fill="y")
    result_listbox.config(yscrollcommand=scrollbar.set)

    for i, res in enumerate(results):
        if response["type"] == "headlines":
            item_text = f"{i+1}. {res['source_name']}: {res['author']} presents - {res['title']}"
        elif response["type"] == "sources":
            item_text = f"{i+1}. {res['source_name']}"
        result_listbox.insert("end", item_text)

    def on_select(event):
        selected_index = result_listbox.curselection()  # Get the index of the selected item
        if selected_index:
            selected_result = results[selected_index[0]]
            display_details(response["type"], selected_result,response)

    result_listbox.bind("<<ListboxSelect>>", on_select)

    back_button = ck.CTkButton(app, text="Back to main menu", command=lambda: [listbox_frame.destroy(), handle_main()])
    back_button.pack(pady=5)
    action_buttons.append(back_button)

def display_details(result_type, result,response):
    clearingButtons()
    output_text.delete("1.0", "end")  # Clear the output box

    output_text.insert("end", "𑁍Details\n")
    if result_type == "headlines":
        output_text.insert("end", f"Source: {result['source_name']}\n")
        output_text.insert("end", f"Author: {result['author']}\n")
        output_text.insert("end", f"Title: {result['title']}\n")
        output_text.insert("end", f"URL: {result['url']}\n")
        output_text.insert("end", f"Published on: {result['publish_date']}\n")
        output_text.insert("end", f"Published at: {result['publish_time']}\n")
    elif result_type == "sources":
        output_text.insert("end", f"Source Name: {result['source_name']}\n")
        output_text.insert("end", f"Coutry: {result['country']}\n")
        output_text.insert("end", f"Description: {result['description']}\n")
        output_text.insert("end", f"URL: {result['url']}\n")
        output_text.insert("end", f"Category: {result['category']}\n")
        output_text.insert("end", f"Language: {result['language']}\n")

    back_button = ck.CTkButton(app, text="Back to results", command=lambda: [clearingButtons(), display_results(response)])
    back_button.pack(pady=5)
    action_buttons.append(back_button)    

    back_button = ck.CTkButton(app, text="Back to main menu", command=lambda: [clearingButtons(), handle_main()])
    back_button.pack(pady=5)
    action_buttons.append(back_button)

#--------------------------Headline handling-------------------
def handle_headlines():
    clearingButtons()
    output_text.insert("end", "𑁍Select a headline menu button option\n")
    for index, item in enumerate(HSUBMENU):
        button = ck.CTkButton(app, text=item, command=lambda index=index: handle_headline_action(index))
        button.pack(pady=5)
        action_buttons.append(button)

def handle_headline_action(action):
    clearingButtons()

    if action == 0:  # Search by Keyword
        user_inp("-Enter Keyword:", process_headline_input, action)
    elif action == 1:  # Search by Category
        handle_category_selection("headlines")
    elif action == 2:  # Search by Country
        handle_country_selection("headlines")
    elif action == 3:  # List all
        handle_req("headlines", action, "List all")
        handle_main()  # Return to the main menu
    elif action == 4:  # Back to main menu
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

    back_button = ck.CTkButton(app, text="Back to headlines", command=lambda: [input_frame.forget(),handle_headlines()])
    back_button.pack(pady=5)
    action_buttons.append(back_button)


def process_headline_input(input_keyword, action):
    keyword = input_keyword.strip()  # Store the entered keyword
    if keyword:
        handle_req("headlines", action, keyword)  # Use handle_req to send the request
        handle_main()  # Return to the main menu after handling the input
    else:
        output_text.insert("end", "Keyword cannot be empty!\n")

#--------------------------Sources handling-------------------
def handle_sources():
    clearingButtons()
    output_text.insert("end", "𑁍Sources Menu\n")
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
        handle_main()  
    elif action == 4:  
        handle_main()

def handle_language_selection():
    clearingButtons()
    output_text.insert("end", "𑁍Languages\n")
    for index, language in enumerate(LANGUAGES):
        button = ck.CTkButton(app, text=language, command=lambda index=index, type=type: language_selected(index))
        button.pack(pady=5)
        action_buttons.append(button)

    back_button = ck.CTkButton(app, text="Back to Sources", command=handle_sources)
    back_button.pack(pady=5)
    action_buttons.append(back_button)

def language_selected(index):
    parameter = LANGUAGES[index]
    handle_req("sources", 2, parameter)
    handle_main()

#--------------------------Shared functions-------------------
def handle_category_selection(type):
    clearingButtons()
    output_text.insert("end", "𑁍Categories\n")
    for index, category in enumerate(CATEGORIES):
        button = ck.CTkButton(app, text=category, command=lambda index=index, type=type: category_selected(index,type))
        button.pack(pady=5)
        action_buttons.append(button)
    dynamicBack(type)

def category_selected(index,type):
    parameter = CATEGORIES[index]
    if type == "headlines":
        action=1
    else:
        action=0     
    handle_req(type,action,parameter)
    handle_main()  # Go back to main menu after handling

def handle_country_selection(type):
    clearingButtons()
    output_text.insert("end", "𑁍Countries\n")
    for index, country in enumerate(COUNTRIES):
        button = ck.CTkButton(app, text=country, command=lambda index=index, type=type: country_selected(index,type))
        button.pack(pady=5)
        action_buttons.append(button)
    dynamicBack(type)

def country_selected(index,type):
    parameter = COUNTRIES[index]
    if type == "headlines":
        action=2
    else:
        action=1    
    handle_req(type,action,parameter)
    handle_main()

#--------------------------Helper functions-------------------
def clearingButtons():
    for button in action_buttons:
        button.pack_forget()

    for widget in dynamic_widgets:
        widget.destroy()
    dynamic_widgets.clear()    

def dynamicBack(type):
    if type=="headlines":
        back_button = ck.CTkButton(app, text="Back to headlines menu", command=handle_headlines)
    else:
        back_button = ck.CTkButton(app, text="Back to sources menu", command=handle_sources)
    back_button.pack(pady=5)
    action_buttons.append(back_button)


app.mainloop()
