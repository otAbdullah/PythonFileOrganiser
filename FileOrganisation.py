import customtkinter, os, shutil, watchdog, time, pyglet, logging
from shutil import move
from os import scandir, rename
from os.path import splitext, exists, join
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image, ImageTk
from customtkinter import filedialog

customtk = customtkinter
titleFont = ("Futura", 32, "bold")
navFont = ("arial", 32, "bold")
pholderText = ("arial", 12, "italic")
selected_dir = "-=-=( Please select your desired folder's directory )=-=-"

sourceDir = selected_dir
soundDir = ""
musicDir = ""
videoDir = ""
imageDir = ""
documentDir = ""
zipfileDir = ""
#miscDir = "" - will be done at a later date

imageExtensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]

videoExtensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

audioExtensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]

documentExtensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

zipfileExtensions = [".zip", ".tar", ".gz", ".z", ".zipx"]


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1

    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        uniqueName = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, uniqueName)
        rename(oldName, newName)
    move(entry, dest)

class FileTransportHandler(FileSystemEventHandler):

    def on_modified(self, event):
        with scandir(sourceDir) as entries:
            for entry in entries:
                name = entry.name
                self.check_sound_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)
                self.check_zip_files(entry, name)


    def check_sound_files(self, entry, name):
        for audioExtension in audioExtensions:
            if name.endswith(audioExtension) or name.endswith(audioExtension.upper()):
                if entry.stat().st_size < 10_000_000 or "SFX" in name:
                    dest = soundDir
                else:
                    dest = musicDir
                move_file(dest, entry, name)
                logging.info(f"Audio File Moved! ({name})")

    def check_video_files(self, entry, name):
        for videoExtension in videoExtensions:
            if name.endswith(videoExtension) or name.endswith(videoExtension.upper()):
                move_file(videoDir, entry, name)
                logging.info(f"Video File Moved! ({name})")

    def check_image_files(self, entry, name):
        for imageExtension in imageExtensions:
            if name.endswith(imageExtension) or name.endswith(imageExtension.upper()):
                move_file(imageDir, entry, name)
                logging.info(f"Image File Moved! ({name})")

    def check_document_files(self, entry, name):
        for documentExtension in documentExtensions:
            if name.endswith(documentExtension) or name.endswith(documentExtension.upper()):
                move_file(documentDir, entry, name)
                logging.info(f"Document File Moved! ({name})")

    def check_zip_files(self, entry, name):
        for zipfileExtension in zipfileExtensions:
            if name.endswith(zipfileExtension) or name.endswith(zipfileExtension.upper()):
                move_file(zipfileDir, entry, name)
                logging.info(f"Zip File Moved! ({name})")















class App(customtk.CTk):
    def __init__(self):
        super().__init__()
        


        self.geometry("1000x300")


        self.labelTitle = customtk.CTkLabel(self, text= "File Organiser / Sorter", text_color="#fff", bg_color="#181414", font=titleFont)
        self.labelTitle.grid(row=0, column=0, columnspan=2, pady=(10, 50))
        self.grid_columnconfigure(0, weight=1)

        self.buttonSet_dir = customtk.CTkButton(self, text="Browse", bg_color="#181414", corner_radius=0, border_width=0, fg_color="#302c34", hover_color="#201c24", command=self.browse_folder)
        self.buttonSet_dir.grid(row=1, column=0, padx=(50, 20), sticky="w", columnspan=2)

        self.entrydir = customtk.CTkLabel(self, text=selected_dir, bg_color="#181414", text_color="#fff", corner_radius=0, fg_color="#302c34", font=pholderText)
        self.entrydir.grid(row=1, column=0, sticky="ew", columnspan=2, padx=(200, 50))
        self.entrydir.bind("<FocusIn>", self.clear_entry)

        self.exitApp = customtk.CTkButton(self, text="x", text_color="#fff", font=navFont, width=25, corner_radius=0, fg_color="transparent", bg_color="#181414", hover_color="#181414", command=self.close_app)
        self.exitApp.place(relx=.96, rely=.01)
        self.exitApp.bind("<Enter>", lambda event: self.exitApp.configure(cursor="hand2"))
        self.exitApp.bind("<Leave>", lambda event: self.exitApp.configure(cursor=""))

        githubLogo = self.load_and_display_icon("github-mark-white.png", 40, 40)
        customtk.CTkLabel(self, image=githubLogo, text="", bg_color="#181414").grid(row=2, column=0, sticky="sw", padx=50, pady=20)

        discordLogo = self.load_and_display_icon("icon_clyde_white_RGB.png", 48, 38)
        customtk.CTkLabel(self, image=discordLogo, text="", bg_color="#181414").grid(row=2, column=0, sticky="sw", padx=110, pady=20)

        twitterLogo = self.load_and_display_icon("logo-white.png", 36, 36)
        customtk.CTkLabel(self, image=twitterLogo, text="", bg_color="#181414").grid(row=2, column=0, sticky="sw", padx=180, pady=20)
        self.grid_rowconfigure(2, weight=1)

        self.startSort = customtk.CTkButton(self, text="SORT!", text_color="#fff", corner_radius=0, bg_color="#d03404", fg_color="#ff3c04", hover_color="#201c24")
        self.startSort.grid(row=2, column=1, sticky="se", padx=50, pady=20)

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
        if folder_path:
            self.entrydir.configure(text="")  # Clear the entry widget
            self.entrydir.configure(text=selected_dir)

    def close_app(self):
        self.destroy()

    def clear_entry(self, event):
        self.entrydir.delete(0, customtk.END)

    def load_and_display_icon(self, file_path, width, height):
        # Load the image
        image = Image.open(file_path)
        # Resize the image if needed
        image = image.resize((width, height))
        # Convert the image to Tkinter PhotoImage format
        tk_image = ImageTk.PhotoImage(image)

        return tk_image

if __name__ == "__main__":
    app = App()
    app.mainloop()

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sourceDir
    event_handler = FileTransportHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()