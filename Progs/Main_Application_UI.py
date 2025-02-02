import sys
import Main_Functions
from Main_Functions import ct
from pathlib import Path
import tkinter
import threading

# Import all critical TKinter elements
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, filedialog, ttk

# Global pathing parameters
FILE_PATH = Path(__file__).parent
ASSETS_PATH = FILE_PATH / "assets" / "frame0"
ICON_PATH = FILE_PATH / "pictures" / "button_Small.png"

def instruction_message_terminal(event):
    message_label = tkinter.Label(window, text="The terminal will display every action performed by the program, as well as any encountered errors!", bg="lightblue", fg="blue")
    message_label.place(x=29, y=398) # Positioning
    message_label.after(500, message_label.destroy) # Display duration

def instruction_message_input(event):
    message_label = tkinter.Label(window, text="Please kindly provide the original spreadsheet (.xls, .xlsx) \ncontaining the list of research papers with their associated abstracts.", bg="lightblue", fg="blue")
    message_label.place(x=326, y=286) # Positioning
    message_label.after(500, message_label.destroy) # Display duration

def instruction_message_llm_selection(event):
    message_label = tkinter.Label(window, text="Please kindly choose the desired LLM from Google. \nFor example, gemini-1.5-flash or gemini-1.0-pro...", bg="lightblue", fg="blue")
    message_label.place(x=326, y=209) # Positioning
    message_label.after(500, message_label.destroy) # Display duration

def instruction_message_api_input(event):
    message_label = tkinter.Label(window, text="Please kindly provide your Google API key.", bg="lightblue", fg="blue")
    message_label.place(x=326, y=133) # Positioning
    message_label.after(500, message_label.destroy) # Display duration

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Configure Tkinter as main Window
window = Tk()
window.title("Automated Conference Decision-Making Systems: Distributing accepted papers into sessions")

window.geometry("800x533")
window.configure(bg = "#9fd0f5")

canvas = Canvas(
    window,
    bg = "#9fd0f5",
    height = 533,
    width = 800,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    400.0,
    266.0,
    image=image_image_1
)

# Terminal box
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    400.0,
    473.0,
    image=entry_image_1
)
entry_1 = Text(
    bd=0,
    bg="#000000",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=29.0,
    y=428.0,
    width=742.0,
    height=88.0
)
entry_1.bind("<Enter>", instruction_message_terminal)

# Input Spreadsheet
entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    553.0,
    267.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=386.0,
    y=256.0,
    width=334.0,
    height=20.0
)
entry_2.bind("<Enter>", instruction_message_input)

# Browse spreadsheet file
file_path = None
def browse_ss():
    global file_path
    file_path = filedialog.askopenfilename(
            title="Select Abstracts List",
            filetypes=[("Excel files", "*.xlsx;*.xls;*.csv")]
    )
    if file_path:
        entry_2.delete(0, "end")
        entry_2.insert(0, file_path)
    print(f"{ct()} - Use data retrieved from {file_path}.")
    return file_path

# Browse file button
button_image_2 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=browse_ss,
    relief="flat"
)
button_2.place(
    x=746.0,
    y=244.0,
    width=40.0,
    height=40.0
)

# LLM Selection box
llm_options = ["gemini-1.5-flash", "gemini-1.5-pro", "palm-2"]

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_3 = canvas.create_image(
    553.0,
    190.0,
    image=entry_image_3
)
entry_3 = ttk.Combobox(
    window,
    values=llm_options,
    state="readonly",
    width=334
)
entry_3.place(
    x=386.0,
    y=179.0,
    width=334.0,
    height=20.0
)
entry_3.bind("<Enter>", instruction_message_llm_selection)

# Save LLM Selection
llm_selection = None
def save_llm_selection():
    global llm_selection
    llm_selection = entry_3.get()
    if not llm_selection:
        messagebox.showwarning("Warning", "No LLM selection detected!")
        return
    print(f"{ct()} - LLM: {llm_selection}, selected!")
    return llm_selection

# LLM Selection button
button_image_4 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=save_llm_selection,
    relief="flat"
)
button_4.place(
    x=746.0,
    y=170.0,
    width=40.0,
    height=40.0
)

# API key input box
entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_4 = canvas.create_image(
    553.0,
    114.99999999999999,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=386.0,
    y=103.99999999999999,
    width=334.0,
    height=20.0
)
entry_4.bind("<Enter>", instruction_message_api_input)

# Save API Key
API_KEY = None
def save_api_key():
    global API_KEY
    API_KEY = entry_4.get()
    if not API_KEY:
        messagebox.showwarning("Warning", "No API Key detected!")
        return
    print(f"{ct()} - API Key: {API_KEY}, provided!")
    return API_KEY

# API Input Button
button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=save_api_key,
    relief="flat"
)
button_3.place(
    x=746.0,
    y=94.99999999999999,
    width=40.0,
    height=40.0
)

# Running main Function
def start_analysis():
    global file_path, llm_selection, API_KEY
    print(f"{ct()} - Data in use: {file_path}, with LLM: {llm_selection} and API Key: {API_KEY}")
    if not file_path:
        messagebox.showwarning("Warning", "No file selected!")
        return
    if not llm_selection:
        messagebox.showwarning("Warning", "No LLM selected!")
        return
    if not API_KEY:
        messagebox.showwarning("Warning", "No API Key provided!")
        return
    print(f"{ct()} - Start analyzing with file: {file_path}, LLM: {llm_selection}, API Key: {API_KEY}")

    # Enable the main process to be performed in Multi-threading mode to avoid UI unresponsiveness
    def process_in_thread():
        Main_Functions.main(file_path, llm_selection, API_KEY)

    thread = threading.Thread(target=process_in_thread)
    thread.start()
    print(f"{ct()} - Started processing in a separate thread.")

# Start button
button_image_1 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=start_analysis,
    relief="flat"
)
button_1.place(
    x=450.0,
    y=330.0,
    width=98.0,
    height=39.20000076293945
)

# Info button
button_image_info = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_info = Button(
    image=button_image_info,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print(f"{ct()} - Created by Nguyen, Son Hoang & Le, Thi Dieu Ly."
                          "\nKindly refer to all source codes and revisions on:"
                          "\nhttps://github.com/sonhoangn/AbstractCategorizationGCSM/tree/master/Progs"
                          "\nUsage: This program leverages Google AI models using Google-provided API key to help analyzing a large data set of abstracts from various research papers, thus helping with putting them into sessions based on their similarity level."),
    relief="flat"
)
button_info.place(
    x=746.0,
    y=350.0,
    width=40.0,
    height=40.0
)

# Redirect stdout to the text area
class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget
    def write(self, string):
        self.text_widget.insert(tkinter.END, string)
        self.text_widget.see(tkinter.END)
        self.text_widget.update_idletasks()
    def flush(self):
        pass

# Set the window icon (cross-platform)
try:
    icon = tkinter.PhotoImage(file=str(ICON_PATH))  # Convert Path to string
    window.iconphoto(True, icon)
except FileNotFoundError:
    print(f"{ct()} - Error: Icon file not found at {ICON_PATH}")
except Exception as e:
    print(f"{ct()} - Error loading icon: {e}")

# Redirect stdout to the text area
class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.text_widget.tag_config("output", foreground="lightblue")  # Configure the tag
    def write(self, string):
        self.text_widget.insert(tkinter.END, string, "output")  # Apply the tag
        self.text_widget.see(tkinter.END)
        self.text_widget.update_idletasks()
    def flush(self):
        pass
sys.stdout = StdoutRedirector(entry_1)

# Welcome Message
print(f"{ct()} - Hello there, please kindly provide all required data before pressing the START button.")

# Lock window resolution
window.resizable(False, False)
window.mainloop()