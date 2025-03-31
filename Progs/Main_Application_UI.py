import sys
import re
import datetime
import Main_Functions
from Main_Functions import ct
from pathlib import Path
import tkinter as tk
from PIL import Image, ImageTk
import threading
import Adjust_Session_Function

# Import all critical TKinter elements
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, filedialog, ttk

# Global parameters
FILE_PATH = Path(__file__).parent
ASSETS_PATH = FILE_PATH / "assets" / "frame0"
ICON_PATH = ASSETS_PATH / "icon.png"
gif_file = FILE_PATH / "assets" / "frame0" / "ls.gif"
gif_logo = FILE_PATH / "assets" / "frame0" / "rls.gif"
gif_x = 933
gif_y = 378
l_x = 6
l_y = 8

def load_gif_frames(filename):
    try:
        img = Image.open(filename)
        frames = []
        delays = []
        try:
            while True:
                # Convert to RGBA to preserve transparency
                rgba_img = img.convert("RGBA")
                frames.append(ImageTk.PhotoImage(rgba_img))
                delays.append(img.info.get('duration', 100))
                img.seek(img.tell() + 1)
        except EOFError:
            pass  # End of GIF frames
        return frames, delays
    except FileNotFoundError:
        print(f"Error: GIF file '{filename}' not found.")
        return [], []

def update_frame(label, frames, delays, index):
    if frames:
        label.config(image=frames[index])
        window.after(delays[index], update_frame, label, frames, delays, (index + 1) % len(frames))
animated_label = None
animated_logo = None
def add_animated_gif(parent, gif_filepath, x, y):
    frames, delays = load_gif_frames(gif_filepath)
    if frames:
        animation_label = tk.Label(parent, bg="#9cacfd")
        animation_label.place(x=x, y=y)
        update_frame(animation_label, frames, delays, 0)
        return animation_label
    else:
        error_label = tk.Label(parent, text="Could not load animated GIF.")
        error_label.place(x=x, y=y)
        return error_label
def add_animated_logo(parent, gif_filepath, x, y):
    frames, delays = load_gif_frames(gif_filepath)
    if frames:
        animation_label = tk.Label(parent, bg="#243468")
        animation_label.place(x=x, y=y)
        update_frame(animation_label, frames, delays, 0)
        return animation_label
    else:
        error_label = tk.Label(parent, text="Could not load animated GIF.")
        error_label.place(x=x, y=y)
        return error_label
def instruction_message_terminal(event):
    global wdlg
    if wdlg == "EN":
        message_label = tk.Label(window, text="The terminal will display every action performed by the program, as well as any encountered errors!", bg="lightblue", fg="blue")
    elif wdlg == "DE":
        message_label = tk.Label(window, text="Das Terminal zeigt jede vom Programm ausgeführte Aktion sowie alle aufgetretenen Fehler an!", bg="lightblue", fg="blue")
    elif wdlg == "VN":
        message_label = tk.Label(window, text="Toàn bộ tương tác và lỗi đều sẽ được hiển thị trên màn hình này!", bg="lightblue", fg="blue")
    message_label.place(x=200, y=398) # Positioning
    # Define entering and leaving object area
    def on_enter(event):
        message_label.after(20000, message_label.destroy)
    def on_leave(event):
        message_label.destroy()
    window.bind("<Enter>", on_enter, add=True)
    window.bind("<Leave>", on_leave, add=True)
    message_label.my_id = window.bind("<Leave>", lambda event: message_label.destroy(), add=True)
    message_label.my_id_enter = window.bind("<Enter>", lambda event: None, add=True)

def instruction_message_input(event):
    global wdlg
    if wdlg == "EN":
        message_label = tk.Label(window, text="Please kindly provide the original spreadsheet (.xls, .xlsx) \ncontaining the list of research papers with their associated abstracts.", bg="lightblue", fg="blue")
    elif wdlg == "DE":
        message_label = tk.Label(window, text="Bitte stellen Sie die Originaltabelle (.xls, .xlsx) mit der Liste \nder Forschungsarbeiten und den dazugehörigen Abstracts zur Verfügung.", bg="lightblue", fg="blue")
    elif wdlg == "VN":
        message_label = tk.Label(window, text="Vui lòng cung cấp bảng dữ liệu gốc (.xls, .xlsx) \ncó chứa danh sách các bài nghiên cứu cùng những bản tóm tắt có liên quan.", bg="lightblue", fg="blue")
    message_label.place(x=429, y=286) # Positioning
    # Define entering and leaving object area
    def on_enter(event):
        message_label.after(20000, message_label.destroy)
    def on_leave(event):
        message_label.destroy()
    window.bind("<Enter>", on_enter, add=True)
    window.bind("<Leave>", on_leave, add=True)
    message_label.my_id = window.bind("<Leave>", lambda event: message_label.destroy(), add=True)
    message_label.my_id_enter = window.bind("<Enter>", lambda event: None, add=True)

def instruction_message_llm_selection(event):
    global wdlg
    if wdlg == "EN":
        message_label = tk.Label(window, text="Please kindly choose the desired Gemini model offered by Google. \nFor example: gemini-1.5-flash, gemini-1.5-pro, gemini-2.0-flash, etc. \nImportant: gemini-1.5-pro can only accommodate up to 50 requests per day per API key, \n and is only suitable for a small data set.", bg="lightblue", fg="blue")
    elif wdlg == "DE":
        message_label = tk.Label(window, text="Bitte wählen Sie das gewünschte LLM. \nBeispiel: gemini-1.5-flash, gemini-1.5-pro, gemini-2.0-flash usw. \nWichtig: gemini-1.5-pro kann nur bis zu 50 Anfragen pro Tag und API-Schlüssel verarbeiten \n und ist nur für kleine Datensätze geeignet.", bg="lightblue", fg="blue")
    elif wdlg == "VN":
        message_label = tk.Label(window, text="Vui lòng chọn LLM từ danh sách xổ xuống. \nVí dụ: gemini-1.5-flash, gemini-1.5-pro, gemini-2.0-flash, v.v. \nQuan trọng: gemini-1.5-pro chỉ có thể xử lý tối đa 50 yêu cầu mỗi ngày cho mỗi API key, \nvà chỉ phù hợp với bộ dữ liệu nhỏ.", bg="lightblue", fg="blue")
    message_label.place(x=429, y=209) # Positioning
    # Define entering and leaving object area
    def on_enter(event):
        message_label.after(20000, message_label.destroy)
    def on_leave(event):
        message_label.destroy()
    window.bind("<Enter>", on_enter, add=True)
    window.bind("<Leave>", on_leave, add=True)
    message_label.my_id = window.bind("<Leave>", lambda event: message_label.destroy(), add=True)
    message_label.my_id_enter = window.bind("<Enter>", lambda event: None, add=True)

def instruction_message_api_input(event):
    global wdlg
    if wdlg == "EN":
        message_label = tk.Label(window, text="Please kindly provide your Google API key.", bg="lightblue", fg="blue")
    elif wdlg == "DE":
        message_label = tk.Label(window, text="Bitte geben Sie Ihren Google API-Schlüssel an.", bg="lightblue", fg="blue")
    elif wdlg == "VN":
        message_label = tk.Label(window, text="Vui lòng cung cấp Gemini API key của bạn tại đây.", bg="lightblue", fg="blue")
    message_label.place(x=429, y=133) # Positioning
    # Define entering and leaving object area
    def on_enter(event):
        message_label.after(20000, message_label.destroy)
    def on_leave(event):
        message_label.destroy()
    window.bind("<Enter>", on_enter, add=True)
    window.bind("<Leave>", on_leave, add=True)
    message_label.my_id = window.bind("<Leave>", lambda event: message_label.destroy(), add=True)
    message_label.my_id_enter = window.bind("<Enter>", lambda event: None, add=True)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def ct():
    crtm = datetime.datetime.now()
    return crtm.strftime("%Y-%m-%d %H:%M:%S")

# Language Toggle
class ImageButton(tk.Button):
    def __init__(self, master, image_paths, **kwargs):  # Take a list of image paths
        self.images = [PhotoImage(file=path) for path in image_paths]
        super().__init__(master, image=self.images[0], **kwargs)
        self.config(compound="center")
        self.current_image = 0

    def switch_image(self):
        self.current_image = (self.current_image + 1) % len(self.images) # Cycle through images
        self.config(image=self.images[self.current_image])
        self.image = self.images[self.current_image]

# Background Toggle
def switch_background():
    global image_image_1
    images = [image_image_1_EN, image_image_1_DE, image_image_1_VI]
    current_index = images.index(image_image_1)
    next_index = (current_index + 1) % len(images)
    image_image_1 = images[next_index]
    canvas.itemconfig(image_1, image=image_image_1)
    canvas.image = image_image_1 # Keep reference

# Title Toggle
def switch_title():
    global current_title_index
    global wdlg
    current_title_index = (current_title_index + 1) % len(titles)
    window.title(titles[current_title_index])
    wdlg = lg[current_title_index]

titles = ["Automated Conference Decision-Making Systems: Distributing accepted papers into sessions",
          "Automatische Konferenzplanung: Zuordnung akzeptierter Beiträge zu Sitzungen",
          "Hệ thống lên lịch Hội Thảo: Sắp xếp chương trình cho các bài nghiên cứu được chấp thuận"]

lg = ["EN", "DE", "VN"]

current_title_index = 0

# Global default parameters
request_delay = 12
role = "You are an expert in sustainable manufacturing that is excellent with analyzing research paper abstracts. Your primary goal is to categorize the abstracts based on predefined topics and provide specific information in a structured format."
s_instructions = """1. Analyze the provided abstract and determine the most appropriate "Overall Category."  This category *must* be chosen from one of the following four predefined topics. Do not create new categories.
            2. Identify the specific "Field of Research" that best describes the abstract. This field *must* be chosen from the sub-topics listed under the chosen "Overall Category." Do not create new sub-topics.
            3. Identify the primary "Research Method" used in the research described in the abstract.  Provide a concise answer (no more than three words).
            4. Assess the "Scope" of the research. Assign a score from 1 to 6 (1 = extremely narrow, 6 = extremely broad).
            5. Determine the "Research Purpose."  Is the research primarily "Theoretical" or "Applied"?
            6. Forecast the "Presentation Time" needed for the topic. Choose either "Brief" (less than 10 minutes) or "Long" (up to 15 minutes).
            7. Provide the "Prompt token count" and "Response token count" for billing and troubleshooting."""

window = tk.Tk()
window.title(titles[current_title_index])
wdlg = "EN"
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
# Initialize background images
image_image_1_EN = PhotoImage(file=relative_to_assets("bg.png"))
image_image_1_DE = PhotoImage(file=relative_to_assets("bg_DE.png"))
image_image_1_VI = PhotoImage(file=relative_to_assets("bg_VI.png"))
image_image_1 = image_image_1_EN # Start with English version
image_1 = canvas.create_image(
    487.0,
    325.0,
    image=image_image_1
)
canvas.image = image_image_1 # Keep reference

# Initialize button images
button_image_2_EN = PhotoImage(file=relative_to_assets("start.png"))
button_image_2_DE = PhotoImage(file=relative_to_assets("start_DE.png"))
button_image_2_VI = PhotoImage(file=relative_to_assets("start_VI.png"))
button_image_3_EN = PhotoImage(file=relative_to_assets("refine.png"))
button_image_3_DE = PhotoImage(file=relative_to_assets("refine_DE.png"))
button_image_3_VI = PhotoImage(file=relative_to_assets("refine_VI.png"))
button_image_1_EN = PhotoImage(file=relative_to_assets("EN.png"))
button_image_1_DE = PhotoImage(file=relative_to_assets("DE.png"))
button_image_1_VI = PhotoImage(file=relative_to_assets("VI.png"))

# Toggle settings
def configurable_parameters():
    global window, role, s_instructions, request_delay
    window1 = tk.Toplevel(window)
    window1.title("Configuration")
    window1.geometry("975x650")
    window1.configure(bg="#6D7BFA")
    window1.resizable(False, False)

    # Icon loading
    icon_path = relative_to_assets("icon.png").as_posix()
    try:
        icon1 = PhotoImage(file=icon_path)
        window1.iconphoto(True, icon1)
    except Exception as e:
        print(f"{ct()} - Error loading icon: {e}\n")

    canvas1 = Canvas(window1, bg="#6D7BFA", height=650, width=975, bd=0, highlightthickness=0, relief="ridge")
    canvas1.place(x=0, y=0)
    canvas_image_1 = PhotoImage(file=relative_to_assets("config.png").as_posix())
    canvas1.create_image(488.0, 325.0, image=canvas_image_1)
    canvas.image = canvas_image_1

    entry_si = Text(window1, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, wrap="word")
    entry_si.place(x=169.0, y=180.0, width=790.0, height=367.0)
    entry_si.insert("1.0", s_instructions)

    entry_rd = Entry(window1, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_rd.place(x=169.0, y=594.0, width=119.0, height=32.0)
    entry_rd.insert(0, request_delay)

    entry_r = Text(window1, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, wrap="word")
    entry_r.place(x=169.0, y=33.999999999999986, width=780.0, height=92.0)
    entry_r.insert("1.0", role)

    # Save adjusted values
    def save_input():
        global role, s_instructions, request_delay, wdlg
        role = entry_r.get("1.0", tk.END).strip()
        s_instructions = entry_si.get("1.0", tk.END).strip()
        request_delay = entry_rd.get()
        try:
            request_delay = int(request_delay)
        except:
            if wdlg == "EN":
                print(f"{ct()} - Error, request delay must be an integer!\n")
            elif wdlg == "DE":
                print(f"{ct()} - Fehler, die Verzögerung muss eine Ganzzahl sein!\n")
            elif wdlg == "VN":
                print(f"{ct()} - Lỗi, độ trễ phải là số nguyên!\n")
        if wdlg == "EN":
            print(f"{ct()} - All new entries are saved!\n")
        elif wdlg == "DE":
            print(f"{ct()} - Alle neuen Einträge werden gespeichert!\n")
        elif wdlg == "VN":
            print(f"{ct()} - Thông tin điều chỉnh đã được lưu!\n")

    button_image_1 = PhotoImage(file=relative_to_assets("save.png").as_posix())
    save_button = Button(window1, image=button_image_1, borderwidth=0, highlightthickness=0, command=save_input, relief="flat")
    save_button.place(x=827.0, y=588.0, width=116.99999237060547, height=39.20000076293945)
    save_button.image = button_image_1

# Settings button
button_image_7 = PhotoImage(
    file=relative_to_assets("settings.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=configurable_parameters,
    relief="flat"
)
button_7.place(
    x=909.0,
    y=331.0,
    width=40.0,
    height=40.0
)

def info_display():
    global wdlg
    if wdlg == "EN":
        print(f"{ct()} - General Information:"
              "\nKindly refer to all source codes and revisions on:"
              "\nhttps://github.com/sonhoangn/AbstractCategorizationGCSM/tree/master/Progs"
              "\nUsage: This program leverages different Gemini models from Google using Google-provided API key to help analyzing a large data set of abstracts from various research papers, thus helping with grouping them into sessions based on their similarity level.\n"
              "\n - Created by: "
              "\n* Nguyen Son Hoang"
              "\n* Le Thi Dieu Ly"
              "\n - Credits for the testing, validation effort and feedback during development:"
              "\n* Truong Duc Anh"
              "\n* Tran Hoang Duy"
              "\n* Phan Thi Nhu Mai"
              "\n* Nguyen Ngoc Nhu Quynh"
              "\n* Huynh Nam Son"
              "\n* Nguyen Xuan Thao"),
    elif wdlg == "DE":
        print(f"{ct()} - Allgemeine Informationen:"
              "\nBitte beachten Sie alle Quellcodes und Revisionen auf:"
              "\nhttps://github.com/sonhoangn/AbstractCategorizationGCSM/tree/master/Progs"
              "\nVerwendung: Dieses Programm nutzt verschiedene Gemini-Modelle von Google unter Verwendung des von Google bereitgestellten API-Schlüssels, um einen großen Datensatz von Abstracts aus verschiedenen Forschungsarbeiten zu analysieren und sie so anhand ihres Ähnlichkeitsgrades in Sitzungen zu gruppieren.\n"
              "\n - Erstellt von: "
              "\n* Nguyen Son Hoang"
              "\n* Le Thi Dieu Ly"
              "\n - Anerkennung für die Test-, Validierungsbemühungen und das Feedback während der Entwicklung:"
              "\n* Truong Duc Anh"
              "\n* Tran Hoang Duy"
              "\n* Phan Thi Nhu Mai"
              "\n* Nguyen Ngoc Nhu Quynh"
              "\n* Huynh Nam Son"
              "\n* Nguyen Xuan Thao"),

    elif wdlg == "VN":
        print(f"{ct()} - Tổng Quan:"
              "\nVui lòng tham khảo tất cả các mã nguồn và bản sửa đổi trên:"
              "\nhttps://github.com/sonhoangn/AbstractCategorizationGCSM/tree/master/Progs"
              "\nSử dụng: Chương trình này tận dụng các mô hình Gemini khác nhau từ Google bằng cách sử dụng khóa API do Google cung cấp để giúp phân tích những bộ dữ liệu lớn gồm các bản tóm tắt từ nhiều bài báo nghiên cứu khác nhau, từ đó giúp phân loại chúng thành nhiều nhóm dựa trên mức độ tương đồng về mặt nội dung của chúng.\n"
              "\n - Được viết bởi: "
              "\n* Nguyễn Sơn Hoàng"
              "\n* Lê Thị Diệu Ly"
              "\n - Ghi nhận đóng góp trong quá trình phát triển giải pháp:"
              "\n* Trương Đức Anh"
              "\n* Trần Hoàng Duy"
              "\n* Phan Thị Như Mai"
              "\n* Nguyễn Ngọc Như Quỳnh"
              "\n* Huỳnh Nam Sơn"
              "\n* Nguyễn Xuân Thao"),

# Info button
button_image_8 = PhotoImage(
    file=relative_to_assets("info_s.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=info_display,
    relief="flat"
)
button_8.place(
    x=957.0,
    y=59.0,
    width=15.0,
    height=15.0
)

# Processing Time Display (entry_2)
entry_image_2 = PhotoImage(file=relative_to_assets("timedisplay.png"))
entry_bg_2 = canvas.create_image(476.5, 355.0, image=entry_image_2)
entry_2 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_2.place(
    x=429.0,
    y=344.0,
    width=95.0,
    height=20.0
)

# Set window icon
try:
    icon = tk.PhotoImage(file=str(ICON_PATH))  # Convert Path to string
    window.iconphoto(True, icon)
except FileNotFoundError:
    if wdlg == "EN":
        print(f"{ct()} - Error: Icon file not found at {ICON_PATH}\n")
    elif wdlg == "DE":
        print(f"{ct()} - Fehler: Symboldatei nicht gefunden unter {ICON_PATH}\n")
    elif wdlg == "VN":
        print(f"{ct()} - Lỗi: Không tìm thấy tệp biểu tượng tại {ICON_PATH}\n")
except Exception as e:
    if wdlg == "EN":
        print(f"{ct()} - Error loading icon: {e}\n")
    elif wdlg == "DE":
        print(f"{ct()} - Fehler beim Laden des Symbols: {e}\n")
    elif wdlg == "VN":
        print(f"{ct()} - Lỗi khi tải biểu tượng: {e}\n")

# Running Main_Functions
def start_analysis():
    global file_path, llm_selection, API_KEY, wdlg, role, s_instructions, request_delay
    if wdlg == "EN":
        print(f"{ct()} - Data in use: {file_path}, with LLM: {llm_selection} and API Key: {API_KEY}\n")
    elif wdlg == "DE":
        print(f"{ct()} - Verwendete Daten: {file_path}, mit LLM: {llm_selection} und API-Schlüssel: {API_KEY}\n")
    elif wdlg == "VN":
        print(f"{ct()} - Dữ liệu đang sử dụng: {file_path}, với LLM: {llm_selection} và API Key: {API_KEY}\n")
    if not file_path:
        messagebox.showwarning("Warning", "No file selected!")
        return
    if not llm_selection:
        messagebox.showwarning("Warning", "No LLM selected!")
        return
    if not API_KEY:
        messagebox.showwarning("Warning", "No API Key provided!")
        return
    if wdlg == "EN":
        print(f"{ct()} - Start analyzing with file: {file_path}, LLM: {llm_selection}, API Key: {API_KEY}\n")
    elif wdlg == "DE":
        print(f"{ct()} - Analyse gestartet mit Datei: {file_path}, LLM: {llm_selection}, API-Schlüssel: {API_KEY}\n")
    elif wdlg == "VN":
        print(f"{ct()} - Bộ dữ liệu sẽ được phân tích: {file_path}, LLM: {llm_selection}, API Key: {API_KEY}\n")

    # Enable the main process to be performed in Multi-threading mode to avoid UI unresponsiveness
    def process_in_thread():
        Main_Functions.main(file_path, llm_selection, API_KEY, wdlg, role, s_instructions, request_delay)

    thread = threading.Thread(target=process_in_thread)
    thread.start()

    if wdlg == "EN":
        print(f"{ct()} - Started processing in a separate thread.\n")
    elif wdlg == "DE":
        print(f"{ct()} - Die Verarbeitung wurde in einem separaten Thread gestartet.\n")
    elif wdlg == "VN":
        print(f"{ct()} - Tác vụ đã được bắt đầu trên một luồng (thread) riêng.\n")

# Start Button
button_2 = ImageButton(window, [relative_to_assets("start.png"), relative_to_assets("start_DE.png"), relative_to_assets("start_VI.png")])
button_2.place(x=575.0, y=335.0, width=112.99999237060547, height=39.20000076293945)
button_2.config(command=start_analysis, relief="flat")

# Run Refine function
def Refine():
    Adjust_Session_Function.main()
    if wdlg == "EN":
        print(f"\n{ct()} - Refining sessions completes...\n")
    elif wdlg == "DE":
        print(f"\n{ct()} - Die Verfeinerung ist fertig …\n")
    elif wdlg == "VN":
        print(f"\n{ct()} - Tinh chỉnh hoàn tất...\n")


# Refine Button
button_3 = ImageButton(window, [relative_to_assets("refine.png"), relative_to_assets("refine_DE.png"), relative_to_assets("refine_VI.png")])
button_3.place(x=746.0, y=335.0, width=126.99999237060547, height=39.20000076293945)
button_3.config(command=Refine, relief="flat")

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
    if wdlg == "EN":
        print(f"{ct()} - Use data retrieved from {file_path}.\n")
    elif wdlg == "DE":
        print(f"{ct()} - Die Daten stammen von {file_path}.\n")
    elif wdlg == "VN":
        print(f"{ct()} - Dữ liệu được lấy từ {file_path}.\n")

    return file_path

# Browse file button
button_image_4 = PhotoImage(
    file=relative_to_assets("browse.png"))
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
llm_options = ["gemini-1.5-flash", "gemini-1.5-flash-8b", "gemini-1.5-pro", "gemini-2.0-flash", "gemini-2.0-flash-lite-preview-02-05"]
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
    print(f"{ct()} - LLM: {llm_selection}, selected!\n")
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
    highlightthickness=0,
    show="*" # hide input while typing
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
    entry_4.delete(0, "end")
    entry_4.insert(0, "**************")
    if wdlg == "EN":
        print(f"{ct()} - API Key provided!\n")
    elif wdlg == "DE":
        print(f"{ct()} - API-Schlüssel bereitgestellt!\n")
    elif wdlg == "VN":
        print(f"{ct()} - API Key đã được cung cấp!\n")

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

# Language Toggle Button
button_1 = ImageButton(window, [relative_to_assets("EN.png"), relative_to_assets("DE.png"), relative_to_assets("VI.png")])
button_1.place(x=909.0, y=7.999999999999986, width=40.0, height=40.0)
button_1.config(command=lambda: [
    button_1.switch_image(),
    button_2.switch_image(),
    button_3.switch_image(),
    switch_background(),
    switch_title()
], relief="flat")

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
    bg="#000000",
    fg="#70e4f8",
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
    fg="#70e4f8",
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
    global gif_file, gif_x, gif_y, animated_label
    def __init__(self, text_widget, time_entry):
        self.text_widget = text_widget
        self.time_entry = time_entry
        self.text_widget.tag_config("output", foreground="lightblue")  # Configure the tag
    def write(self, string):
        self.text_widget.insert(tk.END, string, "output")  # Apply the tag
        self.text_widget.see(tk.END)
        self.text_widget.update_idletasks()
        # Extract processing time
        match = re.search(r".*? abstracts processed in (\d+\.\d+) seconds\..*", string)  # Regex search
        match1 = re.search(r".*? Abstracts in (\d+\.\d+) Sekunden\..*", string)
        match2 = re.search(r".*? bản tóm tắt đã được xử lý trong (\d+\.\d+) giây\..*", string)
        match3 = re.search(r"Start analyzing!", string)  # Regex search
        match4 = re.search(r"Die Analyse wird durchgeführt", string)
        match5 = re.search(r"Phân tích đang được tiến hành", string)
        match6 = re.search(r"Final results save to", string)  # Regex search
        match7 = re.search(r"Endgültige Ergebnisse speichern unter", string)
        match8 = re.search(r"Kết quả cuối cùng đã được lưu vào", string)
        if match:
            time = match.group(1)
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, time)
        elif match1:
            time = match1.group(1)
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, time)
        elif match2:
            time = match2.group(1)
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, time)
        elif match3 or match4 or match5:
            global animated_label, animated_logo
            animated_label = add_animated_gif(window, gif_file, gif_x, gif_y)
            animated_logo = add_animated_logo(window, gif_logo, l_x, l_y)
        elif match6 or match7 or match8:
            if animated_label or animated_logo:
                animated_label.place_forget()
                animated_logo.place_forget()
    def flush(self):
        pass
sys.stdout = StdoutRedirector(entry_5, entry_2)

# Welcome Message
print(f"{ct()} - Hello there, please kindly provide all required data before pressing the START button"
    "\n- Press the button on the right of each text box to save the provided info."
    "\n- Required info include: API_KEY, LLM, and path to the original spreadsheet file."
    "\n- START button will begin the preliminary session assignment routine."
    "\n- REFINE button will help to merge the remaining smaller sessions. The results might not always be accurate depending on how many abstracts share the same topic or overall category.\n")

window.resizable(False, False)
window.mainloop()
