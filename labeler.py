'''GUI for the FileVisual program.'''

import threading
import os
from pathlib import Path
import tkinter
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
import cv2

ext_allowed = [".png", ".jpg"]
file_entries = " "

amount_of_entries = 0
current_file = 0
points = []
file_being_read = 0

def file_ext_allowed(file_str, ext_list):
    for ext in ext_list:
        if file_str.endswith(ext):
            return True
        else:
            return False

def get_files_in_dir(directory):
    dir_list = ""
    full_file_paths = []

    for d in os.listdir(directory):
        filename = Path(d).name

        if not file_ext_allowed(filename, ext_allowed):
            continue

        full_file_paths.append(os.path.join(directory, d))
        dir_list += filename
        dir_list += "\n"

    global file_entries
    file_entries = full_file_paths
    global amount_of_entries
    amount_of_entries = len(full_file_paths)

    return dir_list

def mouse_event(event, x,y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN: # left mouse button click event
        global points
        points.append((x,y))

def draw_square():
    global file_entries
    global file_being_read
    file_being_read = cv2.imread(file_entries[current_file])
    cv2.namedWindow(file_entries[current_file], cv2.WINDOW_NORMAL)
    cv2.imshow(file_entries[current_file], file_being_read)

    cv2.setMouseCallback(file_entries[current_file], mouse_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.rectangle(file_being_read, points[0], points[1], (0,0,255), 3)

def main():
    gui = tkinter.Tk()
    gui.resizable(0, 0)
    directory = tkinter.StringVar(gui, value="")
    gui.title("File to Image")
    set_size_and_pos = gui.geometry("710x500+200+200")
    
    scroll_text = scrolledtext.ScrolledText(gui)
    scroll_text.place(width=150, height=300, x=10, y=10)

    directory = tkinter.StringVar(gui, value="")
    current_file_label= tkinter.StringVar(value="Current file: ")
    curr_file_name = tkinter.StringVar(value="")

    def choose_file():
        directory_chosen = tkinter.filedialog.askdirectory()
        files_n_dir = get_files_in_dir(directory_chosen)

        directory.set(files_n_dir)
        curr_file_name.set(file_entries[0])
        scroll_text.delete('1.0', tkinter.END)
        scroll_text.insert(tkinter.INSERT, directory.get());
        
    def lower_pos():
        global current_file
        if current_file != 0:
            current_file -= 1
            curr_file_name.set(file_entries[current_file])
            print(current_file)
            
    def incr_pos():
        global current_file
        print("his is me", amount_of_entries)
        if current_file != amount_of_entries-1:
            current_file += 1
            curr_file_name.set(file_entries[current_file])
            print(current_file)

    scroll_text = scrolledtext.ScrolledText(gui, wrap='none')
    scroll_text.place(width=150, height=300, x=10, y=10)

    tkinter.Label(gui, textvariable=current_file_label).place(x=170, y=10)
    tkinter.Entry(gui, textvariable=curr_file_name).place(width=400, x=280, y=10)
    ttk.Separator(gui, orient="horizontal").place(height=1, width=710, x=0, y=320)
    ttk.Button(gui, text="Directory", command=choose_file).place(height=150, x=10, y=330)
    ttk.Button(gui, text="Draw", command=draw_square).place(height=150, width=300, x=100, y=330)
    ttk.Button(gui, text="Up", command=lower_pos).place(height=75, width=275, x=405, y=330)
    ttk.Button(gui, text="Down", command=incr_pos).place(height=70, width=275, x=405, y=410)

    tkinter.mainloop()

if __name__ == "__main__":
    main()
