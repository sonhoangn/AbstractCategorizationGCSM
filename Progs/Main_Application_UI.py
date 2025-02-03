from pathlib import Path
import tkinter
import sys
import datetime
import sys
import re
from re import match

import Main_Functions
from Main_Functions import ct
from pathlib import Path
import tkinter
import threading
import Adjust_Session_Function

# Import all critical TKinter elements
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, filedialog, ttk

# Global pathing parameters
FILE_PATH = Path(__file__).parent
ASSETS_PATH = FILE_PATH / "assets" / "frame0"
ICON_PATH = ASSETS_PATH / "icon.png"

def instruction_message_terminal(event):
    message_label = tkinter.Label(window, text="The terminal will display every action performed by the program, as well as any encountered errors!", bg="lightblue", fg="blue")
    message_label.place(x=200, y=398) # Positioning
    message_label.after(500, message_label.destroy) # Display duration

def instruction_message_input(event):
    message_label = tkinter.Label(window, text="Please kindly provide the original spreadsheet (.xls, .xlsx) \ncontaining the list of research papers with their associated abstracts.", bg="lightblue", fg="blue")
    message_label.place(x=429, y=286) # Positioning
    message_label.after(500, message_label.destroy) # Display duration

def instruction_message_llm_selection(event):
    message_label = tkinter.Label(window, text="Please kindly choose the desired LLM from Google. \nFor example, gemini-1.5-flash or gemini-1.0-pro...", bg="lightblue", fg="blue")
    message_label.place(x=429, y=209) # Positioning
    message_label.after(500, message_label.destroy) # Display duration

def instruction_message_api_input(event):
    message_label = tkinter.Label(window, text="Please kindly provide your Google API key.", bg="lightblue", fg="blue")
    message_label.place(x=429, y=133) # Positioning
    message_label.after(500, message_label.destroy) # Display duration

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def ct():
    return datetime.datetime.now()

window = Tk()
window.title("Automated Conference Decision-Making Systems: Distributing accepted papers into sessions")

window.geometry("975x650")
window.configure(bg = "#9fd0f5")


canvas = Canvas(
    window,
    bg = "#9fd0f5",
    height = 650,
    width = 975,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("bg.png"))
image_1 = canvas.create_image(
    487.0,
    325.0,
    image=image_image_1
)

# Processing Time Display (entry_2)
entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(476.5, 355.0, image=entry_image_2)
entry_2 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_2.place(x=422.0, y=344.0, width=109.0, height=20.0)

# Set the window icon (cross-platform)
try:
    icon = tkinter.PhotoImage(file=str(ICON_PATH))  # Convert Path to string
    window.iconphoto(True, icon)
except FileNotFoundError:
    print(f"{ct()} - Error: Icon file not found at {ICON_PATH}")
except Exception as e:
    print(f"{ct()} - Error loading icon: {e}")

# Info button
button_image_1 = PhotoImage(
    file=relative_to_assets("info.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print(f"{ct()} - Created by Nguyen, Son Hoang & Le, Thi Dieu Ly."
                          "\nKindly refer to all source codes and revisions on:"
                          "\nhttps://github.com/sonhoangn/AbstractCategorizationGCSM/tree/master/Progs"
                          "\nUsage: This program leverages Google AI models using Google-provided API key to help analyzing a large data set of abstracts from various research papers, thus helping with putting them into sessions based on their similarity level."),
    relief="flat"
)
button_1.place(
    x=909.0,
    y=331.0,
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

# Start Button
button_image_2 = PhotoImage(
    file=relative_to_assets("start.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=start_analysis,
    relief="flat"
)
button_2.place(
    x=575.0,
    y=335.0,
    width=112.99999237060547,
    height=39.20000076293945
)

# Run Refine function
def Refine():
    Adjust_Session_Function.main()
    print(f"\n{ct()} - Refining sessions completes...")

# Refine function button
button_image_3 = PhotoImage(
    file=relative_to_assets("refine.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=Refine,
    relief="flat"
)
button_3.place(
    x=746.0,
    y=335.0,
    width=116.99999237060547,
    height=39.20000076293945
)

# Input Spreadsheet
entry_image_1 = PhotoImage(
    file=relative_to_assets("inputarea.png"))
entry_bg_1 = canvas.create_image(
    650.0,
    267.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=429.0,
    y=256.0,
    width=442.0,
    height=20.0
)
entry_1.bind("<Enter>", instruction_message_input)

# Browse spreadsheet file
file_path = None
def browse_ss():
    global file_path
    file_path = filedialog.askopenfilename(
            title="Select Abstracts List",
            filetypes=[("Excel files", "*.xlsx;*.xls;*.csv")]
    )
    if file_path:
        entry_1.delete(0, "end")
        entry_1.insert(0, file_path)
    print(f"{ct()} - Use data retrieved from {file_path}.")
    return file_path

# Browse file button
button_image_4 = PhotoImage(
    file=relative_to_assets("check.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=browse_ss,
    relief="flat"
)
button_4.place(
    x=909.0,
    y=244.0,
    width=40.0,
    height=40.0
)

# LLM Selection box
llm_options = ["gemini-1.5-flash", "gemini-1.5-pro", "palm-2"]
entry_image_3 = PhotoImage(
    file=relative_to_assets("inputarea.png"))
entry_bg_3 = canvas.create_image(
    650.0,
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
    x=429.0,
    y=179.0,
    width=442.0,
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
button_image_5 = PhotoImage(
    file=relative_to_assets("check.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=save_llm_selection,
    relief="flat"
)
button_5.place(
    x=909.0,
    y=170.0,
    width=40.0,
    height=40.0
)

# API_Key input box
entry_image_4 = PhotoImage(
    file=relative_to_assets("inputarea.png"))
entry_bg_4 = canvas.create_image(
    650.0,
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
    x=429.0,
    y=103.99999999999999,
    width=442.0,
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

# Input API_Key
button_image_6 = PhotoImage(
    file=relative_to_assets("check.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=save_api_key,
    relief="flat"
)
button_6.place(
    x=909.0,
    y=94.99999999999999,
    width=40.0,
    height=40.0
)

# Processing Time Display
entry_image_2 = PhotoImage(
    file=relative_to_assets("timedisplay.png"))
entry_bg_2 = canvas.create_image(
    476.5,
    355.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=422.0,
    y=344.0,
    width=109.0,
    height=20.0
)

# Terminal box
entry_image_5 = PhotoImage(
    file=relative_to_assets("terminal.png"))
entry_bg_5 = canvas.create_image(
    487.0,
    526.5,
    image=entry_image_5
)
entry_5 = Text(
    bd=0,
    bg="#000000",
    fg="#000716",
    highlightthickness=0
)
entry_5.place(
    x=29.0,
    y=427.0,
    width=916.0,
    height=197.0
)
entry_5.bind("<Enter>", instruction_message_terminal)

# Redirect stdout to the terminal area
class StdoutRedirector(object):
    def __init__(self, text_widget, time_entry):
        self.text_widget = text_widget
        self.time_entry = time_entry
        self.text_widget.tag_config("output", foreground="lightblue")  # Configure the tag
    def write(self, string):
        self.text_widget.insert(tkinter.END, string, "output")  # Apply the tag
        self.text_widget.see(tkinter.END)
        self.text_widget.update_idletasks()
        # Extract processing time
        match = re.search(r".*? abstracts processed in (\d+\.\d+) seconds\..*", string)  # Regex search
        if match:
            time = match.group(1)
            self.time_entry.delete(0, tkinter.END)
            self.time_entry.insert(0, time)
    def flush(self):
        pass
sys.stdout = StdoutRedirector(entry_5, entry_2)

# Welcome Message
print(f"""{ct()} - Hello there, please kindly provide all required data before pressing the START button\n
    - Press the button on the right of each text box to save the provided info.\n
    - Required info include: API_KEY, LLM, and path to the original spreadsheet file.\n
    - START button will begin the preliminary session assignment routine.\n
    - REFINE button will help to merge the remaining smaller sessions.""")

window.resizable(False, False)
window.mainloop()
