import customtkinter, os, shutil, watchdog, time, pyglet
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from customtkinter import filedialog

customtk = customtkinter
titleFont = ("Futura", 32, "bold")
navFont = ("arial", 32, "bold")
pholderText = ("arial", 12, "italic")
selected_dir = "-=-=( Please select your desired folder's directory )=-=-"

class App(customtk.CTk):
    def __init__(self):
        super().__init__()
        


        self.geometry("1000x300")


        self.labelTitle = customtk.CTkLabel(self, text= "File Organiser / Sorter", text_color="#fff", bg_color="#181414", font=titleFont)
        self.labelTitle.grid(row=0, column=0, columnspan=2, pady=(10, 50))
        self.grid_columnconfigure(0, weight=1)

        self.buttonSet_dir = customtk.CTkButton(self, text="Browse", bg_color="#181414", corner_radius=0, border_width=0, fg_color="#302c34", hover_color="#201c24", command=self.browse_folder)
        self.buttonSet_dir.grid(row=1, column=0, padx=(50, 20), sticky="w")

        self.entrydir = customtk.CTkLabel(self, text=selected_dir, bg_color="#181414", text_color="#fff", corner_radius=0, fg_color="#302c34", font=pholderText)
        self.entrydir.grid(row=1, column=0, sticky="ew", columnspan=2, padx=(200, 50))
        self.entrydir.bind("<FocusIn>", self.clear_entry)

        self.exitApp = customtk.CTkButton(self, text="x", text_color="#fff", font=navFont, width=25, corner_radius=0, fg_color="transparent", bg_color="#181414", hover_color="#181414", command=self.close_app)
        self.exitApp.place(relx=.96, rely=.01)
        self.exitApp.bind("<Enter>", lambda event: self.exitApp.configure(cursor="hand2"))
        self.exitApp.bind("<Leave>", lambda event: self.exitApp.configure(cursor=""))

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

    def on_enter(self, event):
        self.exitApp.configure(cursor="hand2")  # Change cursor to a pointing hand

    def on_leave(self, event):
        self.exitApp.configure(cursor="")

    def browse_folder(self):
        global selected_dir
        folder_path = filedialog.askdirectory()
        selected_dir = folder_path
        self.entrydir.configure(text="")  # Clear the entry widget
        self.entrydir.configure(text=selected_dir)

    def close_app(self):
        self.destroy()

    def clear_entry(self, event):
        self.entrydir.delete(0, customtk.END)



if __name__ == "__main__":
    app = App()
    app.mainloop()