import os
import shutil
import win32com.client
import tkinter as tk
from tkinter import filedialog

osu_path = os.getenv('APPDATA') + '\\osu'
if not os.path.exists(osu_path):
    osu_path = ""


def select_directory():
    global osu_path
    osu_path = filedialog.askdirectory(initialdir=osu_path)
    osu_path_entry.delete(0, tk.END)
    osu_path_entry.insert(tk.END, osu_path)


def extract_osu_music():
    target_path = os.getcwd() + '\\osu_music'
    file_size = 1500000

    status_label.config(text="Extracting OSU music...")
    window.update()  # Update the window to display the status message

    for root, dirs, files in os.walk(osu_path):
        for file in files:
            if os.path.getsize(os.path.join(root, file)) > file_size:
                if not os.path.exists(target_path):
                    os.makedirs(target_path)
                shutil.copy(os.path.join(root, file), target_path)

                if not os.path.splitext(os.path.join(target_path, file))[1]:
                    os.rename(os.path.join(target_path, file),
                              os.path.join(target_path, file + '.mp3'))
                    try:
                        mp3 = win32com.client.Dispatch("WMPlayer.OCX")
                        mp3_file = mp3.newMedia(
                            os.path.join(target_path, file + '.mp3'))
                        mp3_name = mp3_file.getItemInfo('Title')
                        os.rename(os.path.join(target_path, file + '.mp3'),
                                  os.path.join(target_path, mp3_name + '.mp3'))

                    except:
                        status_label.config(text="Error: File not renamed")
                        window.update()
                        pass
                status_label.config(text=os.path.join(target_path, file))
                window.update()

    for root, dirs, files in os.walk(target_path):
        for file in files:
            if not os.path.splitext(os.path.join(root, file))[1] == '.mp3':
                os.remove(os.path.join(root, file))
                status_label.config(text="Removed: " +
                                    os.path.join(root, file))
                window.update()

    status_label.config(text="Extraction complete.")
    window.update()


# Create the main window
window = tk.Tk()
window.title("OSU Music Extractor")

# Directory selection
osu_path_label = tk.Label(window, text="OSU Directory:")
osu_path_label.pack()
osu_path_entry = tk.Entry(window, width=50)
osu_path_entry.pack(side=tk.LEFT)
osu_path_entry.insert(tk.END, osu_path)
osu_path_button = tk.Button(
    window, text="Select Directory", command=select_directory)
osu_path_button.pack(side=tk.LEFT)

# Extract button
extract_button = tk.Button(
    window, text="Extract OSU Music", command=extract_osu_music)
extract_button.pack()

# Status label
status_label = tk.Label(window, text="")
status_label.pack()

# Start the GUI event loop
window.mainloop()
