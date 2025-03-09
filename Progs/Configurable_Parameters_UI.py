from pathlib import Path
import os
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import datetime
from Main_Functions import role, s_instructions, request_delay

SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
ASSETS_PATH = SCRIPT_DIR / "assets" / "frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def ct():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    window = Tk()
    window.title("Configuration")
    window.geometry("975x650")
    window.configure(bg="#6D7BFA")
    window.resizable(False, False)

    # Icon loading
    icon_path = relative_to_assets("icon.png").as_posix()
    print(f"{icon_path}")
    try:
        icon = PhotoImage(file=icon_path)
        window.iconphoto(True, icon)
    except Exception as e:
        print(f"{ct()} - Error loading icon: {e}\n")

    canvas = Canvas(window, bg="#6D7BFA", height=650, width=975, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    print(f"{relative_to_assets("config.png").as_posix()}")
    image_image_1 = PhotoImage(file=relative_to_assets("config.png").as_posix())
    canvas.create_image(488.0, 325.0, image=image_image_1)
    canvas.image = image_image_1
    print(f"{relative_to_assets("save.png").as_posix()}")
    button_image_1 = PhotoImage(file=relative_to_assets("save.png").as_posix())
    save_button = Button(window, image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: print("Saved!"), relief="flat")
    save_button.place(x=827.0, y=588.0, width=116.99999237060547, height=39.20000076293945)
    save_button.image = button_image_1

    entry_1 = Text(window, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, wrap="word")
    entry_1.place(x=164.0, y=180.0, width=790.0, height=367.0)

    entry_2 = Entry(window, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_2.place(x=169.0, y=594.0, width=119.0, height=32.0)

    entry_3 = Text(window, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, wrap="word")
    entry_3.place(x=169.0, y=33.999999999999986, width=780.0, height=92.0)

    window.mainloop()

if __name__ == "__main__":
    main()