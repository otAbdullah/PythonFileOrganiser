import customtkinter as customtk
import os, shutil, watchdog, time, pyglet, logging, threading, sys, webbrowser
from shutil import move
from os import scandir, rename
from os.path import splitext, exists, join
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image, ImageTk
from customtkinter import filedialog
from tkinter import messagebox
import ctypes
from ctypes import windll


GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

titleFont = ("Futura", 32, "bold")
navFont = ("arial", 32, "bold")
pholderText = ("arial", 12, "italic")
#miscDir = "" - will be done at a later date

selected_dir = "-=-=( Please select your desired folder's directory )=-=-"
soundDir = (selected_dir + "/Sounds")
musicDir = (selected_dir + "/Music")
videoDir = (selected_dir + "/Videos")
imageDir = (selected_dir + "/Images")
documentDir = (selected_dir + "/Documents")
zipfileDir = (selected_dir + "/Zip_Files")
    
imageExtensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]

videoExtensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

audioExtensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]

documentExtensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

zipfileExtensions = [".zip", ".tar", ".gz", ".z", ".zipx"]



def set_appwindow(self):
    hwnd = windll.user32.GetParent(self.winfo_id())
    style = windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)
    self.withdraw()
    self.after(10, self.deiconify)


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1

    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

def move_file(dest, entry, name):
    max_attempts = 5
    attempts = 0
    while attempts < max_attempts:
        try:
            if exists(f"{dest}/{name}"):
                uniqueName = make_unique(dest, name)
                oldName = join(dest, name)
                newName = join(dest, uniqueName)
                rename(oldName, newName)
            move(entry, dest)
            break
        except PermissionError:
            attempts += 1
            time.sleep(1)
    
    if attempts == max_attempts:
        logging.error(f"Failed to move file after {max_attempts} attempts: {name}")

class FileTransportHandler(FileSystemEventHandler):


    def on_modified(self, event):
        with scandir(selected_dir) as entries:
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
        
        self.running = False
        self.observer = None
        self.popup_count = 0

        self.geometry("1000x300")
        self.wm_overrideredirect(True)
        self.config(bg="#181414", highlightbackground="#ff3c04", highlightcolor="#ff3c04", highlightthickness=1)
        self.wm_title("=_otAbdullah's File Organiser_=")
        self.wm_iconbitmap("Images/Icon.ico")
        self.after(10, set_appwindow, self)


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

        github_logo = self.load_and_display_icon("Images/github-mark-white.png", 40, 40)
        github_label = customtk.CTkLabel(self, image=github_logo, text="", bg_color="#181414")
        github_label.grid(row=2, column=0, sticky="sw", padx=50, pady=20)
        github_label.bind("<Button-1>", lambda event: self.on_github_click())
        github_label.bind("<Enter>", lambda event: self.change_cursor("hand2"))
        github_label.bind("<Leave>", lambda event: self.change_cursor(""))

        discord_logo = self.load_and_display_icon("Images/icon_clyde_white_RGB.png", 48, 38)
        discord_label = customtk.CTkLabel(self, image=discord_logo, text="", bg_color="#181414")
        discord_label.grid(row=2, column=0, sticky="sw", padx=110, pady=20)
        discord_label.bind("<Button-1>", lambda event: self.on_discord_click())
        discord_label.bind("<Enter>", lambda event: self.change_cursor("hand2"))
        discord_label.bind("<Leave>", lambda event: self.change_cursor(""))

        twitter_logo = self.load_and_display_icon("Images/logo-white.png", 36, 36)
        twitter_label = customtk.CTkLabel(self, image=twitter_logo, text="", bg_color="#181414")
        twitter_label.grid(row=2, column=0, sticky="sw", padx=180, pady=20)
        twitter_label.bind("<Button-1>", lambda event: self.on_twitter_click())
        twitter_label.bind("<Enter>", lambda event: self.change_cursor("hand2"))
        twitter_label.bind("<Leave>", lambda event: self.change_cursor(""))

        self.grid_rowconfigure(2, weight=1)

        self.startSort = customtk.CTkButton(self, text="SORT!", text_color="#fff", corner_radius=0, bg_color="#d03404", fg_color="#ff3c04", hover_color="#201c24", command=self.sort)
        self.startSort.grid(row=2, column=1, sticky="se", padx=50, pady=20)

       # self.startSort = customtk.CTkButton(self, text="check", text_color="#fff", corner_radius=0, bg_color="#d03404", fg_color="#ff3c04", hover_color="#201c24") command=self.check)
       # self.startSort.grid(row=2, column=0, sticky="sw", padx=50, pady=20) - debug

        self.bind("<ButtonPress-1>", self.start_drag)
        self.bind("<B1-Motion>", self.dragging)

    def on_github_click(self):
        print("GitHub icon clicked!")
        webbrowser.open_new_tab("https://github.com/otAbdullah")

    def on_discord_click(self):
        print("Discord icon clicked!")
        webbrowser.open_new_tab("https://otabdullah.github.io/Discord_Name_Tag/")

    def on_twitter_click(self):
        print("Twitter icon clicked!")
        webbrowser.open_new_tab("https://twitter.com/MultiMasteryArc")

    def change_cursor(self, cursor_type):
        self.configure(cursor=cursor_type)

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def dragging(self, event):
        x = self.winfo_x() - self.x + event.x
        y = self.winfo_y() - self.y + event.y
        self.geometry(f"+{x}+{y}")

    def browse_folder(self):
        global selected_dir
        global soundDir
        global musicDir
        global videoDir
        global imageDir
        global documentDir
        global zipfileDir
        folder_path = filedialog.askdirectory()
        if folder_path:
            selected_dir = folder_path
            soundDir = (selected_dir + "/Sounds")
            musicDir = (selected_dir + "/Music")
            videoDir = (selected_dir + "/Videos")
            imageDir = (selected_dir + "/Images")
            documentDir = (selected_dir + "/Documents")
            zipfileDir = (selected_dir + "/Zip_Files")
            self.entrydir.configure(text="")  # Clear the entry widget
            self.entrydir.configure(text=selected_dir)

    def close_app(self):
        self.destroy()
        sys.exit()

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
    
    def error_popup(self):
        if self.popup_count == 0:
            self.popup = customtk.CTkToplevel(self)
            self.popup.title("Dummy")
            self.popup.overrideredirect(True)
            self.popup.config(bg="#181414", highlightbackground="#ff3c04", highlightcolor="#ff3c04", highlightthickness=1)
            self.popup.geometry("300x100")

            label = customtk.CTkLabel(self.popup, text="Please Select A Folder!", font=titleFont, text_color="#fff", bg_color="#181414")
            label.pack(pady=10)
            button = customtk.CTkButton(self.popup, text="OK", corner_radius=0, bg_color="#d03404", fg_color="#ff3c04", hover_color="#201c24", command=self.on_click)
            button.pack()
            self.popup_count += 1

    def on_click(self):
        self.popup_count = 0
        self.popup.destroy()
    
    def sort(self):

        if not selected_dir == ("-=-=( Please select your desired folder's directory )=-=-") and not self.running:
            if not os.path.exists(selected_dir + "/Sounds"):
                os.mkdir(selected_dir + "/Sounds")
            else:
                logging.info(f"Sounds Folder exists")

            if not os.path.exists(selected_dir + "/Music"):
                os.mkdir(selected_dir + "/Music")
            else:
                logging.info(f"Music Folder exists")

            if not os.path.exists(selected_dir + "/Videos"):
                os.mkdir(selected_dir + "/Videos")
            else:
                logging.info(f"Videos Folder exists")

            if not os.path.exists(selected_dir + "/Images"):
                os.mkdir(selected_dir + "/Images")
            else:
                logging.info(f"Images Folder exists")

            if not os.path.exists(selected_dir + "/Documents"):
                os.mkdir(selected_dir + "/Documents")
            else:
                logging.info(f"Documents Folder exists")

            if not os.path.exists(selected_dir + "/Zip_Files"):
                os.mkdir(selected_dir + "/Zip_Files")
            else:
                logging.info(f"Zip Folder exists")

            if self.observer:
                self.observer.stop()
                self.observer.join()

            path = selected_dir
            event_handler = FileTransportHandler()
            self.observer = Observer()
            self.observer.schedule(event_handler, path, recursive=True)
            self.observer.start()

            with scandir(selected_dir) as entries:
                for entry in entries:
                    name = entry.name
                    FileTransportHandler.check_sound_files(self, entry, name)
                    FileTransportHandler.check_video_files(self, entry, name)
                    FileTransportHandler.check_image_files(self, entry, name)
                    FileTransportHandler.check_document_files(self, entry, name)
                    FileTransportHandler.check_zip_files(self, entry, name)

            
        else:
            if selected_dir == ("-=-=( Please select your desired folder's directory )=-=-"):
                self.error_popup()
            
   # SMALL DEBUG
   # def check(self):
   #     print ("hi:" + selected_dir + "this:" + selected_dir)
   #     print ("1:" + soundDir)
   #     print ("1:" + documentDir)
   #     print ("1:" + zipfileDir)

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    app = App()
    app.mainloop()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        app.observer.stop()
        app.observer.join()
