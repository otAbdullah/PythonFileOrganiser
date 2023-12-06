import customtkinter, os, shutil, watchdog, time, pyglet
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from customtkinter import filedialog

customtk = customtkinter
titleFont = ("Futura", 32, "bold")
selected_dir = "Set to desired folder directory"

class App(customtk.CTk):
    def __init__(self):
        super().__init__()
        


        self.geometry("1000x300")


        self.labelTitle = customtk.CTkLabel(self, text= "File Organiser / Sorter", text_color="#fff", bg_color="#181414", font=titleFont)
        self.labelTitle.grid(row=0, column=0, columnspan=2, pady=(10, 50))
        self.grid_columnconfigure(0, weight=1)

        self.buttonSet_dir = customtk.CTkButton(self, text="Browse", bg_color="#181414")
        self.buttonSet_dir.grid(row=1, column=0, padx=(50, 20), sticky="w")

        self.entrydir = customtk.CTkEntry(self, placeholder_text=selected_dir, bg_color="#181414", placeholder_text_color="#fff")
        self.entrydir.grid(row=1, column=0, sticky="ew", columnspan=2, padx=(200, 50))




        self.bind("<ButtonPress-1>", self.start_drag)
        self.bind("<B1-Motion>", self.dragging)

        self.overrideredirect(True)
        self.config(bg="#181414", highlightbackground="#ff3c04", highlightcolor="#ff3c04", highlightthickness=1)

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def dragging(self, event):
        x = self.winfo_x() - self.x + event.x
        y = self.winfo_y() - self.y + event.y
        self.geometry(f"+{x}+{y}")

    def browse_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            selected_dir = file_path



if __name__ == "__main__":
    app = App()
    app.mainloop()