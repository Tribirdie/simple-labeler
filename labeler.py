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

file_entries = [] # will hold all the file paths
file_label_statuses = {}
amount_of_entries = 0 
current_file_index = 0 # tracks current file being operated on
points = [] # holds the clicked that a rectangle will be drawn over

file_being_read = -1 # cv2 matrix
backup_file_cpy = -1

def file_ext_allowed(file_str, ext_list):
    for ext in ext_list:
        if file_str.endswith(ext):
            return True
        else:
            continue

    return False

def get_files_in_dir(directory):
    global file_label_statuses

    dir_list = ""
    full_file_paths = []

    for d in os.listdir(directory):
        filename = Path(d).name

        if not file_ext_allowed(filename, ext_allowed):
            continue

        full_file_directory = os.path.join(directory, d)

        file_label_statuses[full_file_directory] = "False"
        full_file_paths.append(full_file_directory)
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
    global backup_file_cpy
    file_being_read = cv2.imread(file_entries[current_file_index])
    backup_file_cpy = cv2.imread(file_entries[current_file_index])

    cv2.namedWindow(file_entries[current_file_index], cv2.WINDOW_NORMAL)
    cv2.imshow(file_entries[current_file_index], file_being_read)

    cv2.setMouseCallback(file_entries[current_file_index], mouse_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.rectangle(file_being_read, points[0], points[1], (0,0,255), 3)

def preview():
    cv2.namedWindow(file_entries[current_file_index], cv2.WINDOW_NORMAL)
    cv2.imshow(file_entries[current_file_index], file_being_read)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    gui = tkinter.Tk()
    gui.resizable(0, 0)
    directory = tkinter.StringVar(gui, value="")
    gui.title("File to Image")
    set_size_and_pos = gui.geometry("710x500+200+200")
    
    scroll_text = scrolledtext.ScrolledText(gui)
    scroll_text.place(width=150, height=300, x=10, y=10)

    to_stringvar = tkinter.StringVar(value="")

    def choose_file():
        global current_file_index
        directory_chosen = tkinter.filedialog.askdirectory()
        files_n_dir = get_files_in_dir(directory_chosen)

        directory.set(files_n_dir)
        curr_file_name.set(file_entries[0])
        to_stringvar.set(file_label_statuses[file_entries[0]])

        scroll_text.delete('1.0', tkinter.END)
        scroll_text.insert(tkinter.INSERT, directory.get());
        
    def lower_pos():
        global current_file_index
        if current_file_index != 0:
            current_file_index -= 1
            curr_file_name.set(file_entries[current_file_index])
            to_stringvar.set(file_label_statuses[file_entries[current_file_index]])

            print(current_file_index)
            
    def incr_pos():
        global current_file_index
        if current_file_index != amount_of_entries-1:
            current_file_index += 1
            curr_file_name.set(file_entries[current_file_index])
            to_stringvar.set(file_label_statuses[file_entries[current_file_index]])
            print(current_file_index)
            
    def approve():
        cv2.imwrite(file_entries[current_file_index], file_being_read)
        # update file status to indicate it has been drawn over
        file_label_statuses[file_entries[current_file_index]] = "True"
        to_stringvar.set(file_label_statuses[file_entries[current_file_index]])
        
    def reject():
        global file_being_read
        file_being_read = backup_file_cpy
        file_label_statuses[file_entries[current_file_index]] = "False"
        to_stringvar.set(file_label_statuses[file_entries[current_file_index]])

    scroll_text = scrolledtext.ScrolledText(gui, wrap='none')
    scroll_text.place(width=150, height=300, x=10, y=10)

    current_file_label= tkinter.StringVar(value="Current file: ")
    curr_file_name = tkinter.StringVar(value="")

    tkinter.Label(gui, textvariable=current_file_label).place(x=170, y=10)
    tkinter.Entry(gui, textvariable=curr_file_name).place(width=400, x=280, y=10)
    tkinter.Button(gui, text="Preview", command=preview).place(width=200, x=280, y=35)
    tkinter.Button(gui, text="Approve", command=approve).place(width=100, x=480, y=35)
    tkinter.Button(gui, text="Reject", command=reject).place(width=100, x=580, y=35)

    curr_file_status_label = tkinter.StringVar(value="Current file status: ")
    tkinter.Label(gui, textvariable=curr_file_status_label).place(x=170, y=100)

    tkinter.Entry(gui, textvariable=to_stringvar).place(x=300, y=100)

    ttk.Separator(gui, orient="horizontal").place(height=1, width=710, x=0, y=320)
    ttk.Button(gui, text="Directory", command=choose_file).place(height=150, x=10, y=330)
    ttk.Button(gui, text="Draw", command=draw_square).place(height=150, width=300, x=100, y=330)
    ttk.Button(gui, text="Up", command=lower_pos).place(height=75, width=275, x=405, y=330)
    ttk.Button(gui, text="Down", command=incr_pos).place(height=70, width=275, x=405, y=410)

    tkinter.mainloop()

if __name__ == "__main__":
    main()
