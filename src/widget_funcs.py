from pathlib import Path
from pathlib import PurePath
import os
import tkinter
import json
import cv2
from .utility_funcs import get_files_in_dir, make_json, dump_dict_to_json, load_json_if_exists
from .utility_funcs import json_entry_exists

class WidgetFunctions:
    '''Central point for all the functions used in the gui'''
    # GUI is a class that runs the tkinter mainloop.
    # Needed to access StringVars that otherwise cannot be accessed just from here.
    # Some methods like choose_directory and incr_pos need it to function
    def __init__(self, GUI):
        self.GUI = GUI 
        self.ext_allowed = (".png", ".jpg")
        self.file_entries = []

        self.file_label_statuses = {}
        self.amount_of_entries = 0
        self.current_file_index = 0 # tracks current file being operated on
        self.points = [] # holds the clicked that a rectangle will be drawn over

        self.json_file = 1
        self.file_being_read = -1 # cv2 matrix
        self.backup_file_cpy = -1
    
    def mouse_event(self, event, x,y, flags, param):
        '''checks for LMB click'''
        if event == cv2.EVENT_LBUTTONDOWN:
            self.points.append((x,y))

    def draw_square(self):
        '''Draws a square. The changes can be rejected or approved'''
        
        if not os.path.exists(self.file_entries[self.current_file_index]):
            return

        self.file_being_read = cv2.imread(self.file_entries[self.current_file_index])
        # copy in case the user wants to undo the changes
        self.backup_file_cpy = cv2.imread(self.file_entries[self.current_file_index])

        cv2.namedWindow(self.file_entries[self.current_file_index], cv2.WINDOW_NORMAL)
        cv2.imshow(self.file_entries[self.current_file_index], self.file_being_read)

        cv2.setMouseCallback(self.file_entries[self.current_file_index], self.mouse_event)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        try:
            cv2.rectangle(self.file_being_read, self.points[0], self.points[1], (0,0,255), 3)
        except IndexError:
            pass

    def preview(self):
        '''preview the drawn image before applying the changes'''
        cv2.namedWindow(self.file_entries[self.current_file_index], cv2.WINDOW_NORMAL)
        cv2.imshow(self.file_entries[self.current_file_index], self.file_being_read)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def choose_file(self):
        '''Grab all the files in a directory and put them in the scrolledtext as a string'''
        directory_chosen = tkinter.filedialog.askdirectory()

        get_last_dir = directory_chosen.split("/")
        self.json_file = f"label_statuses/{get_last_dir[-1]}.json"
        if not os.path.exists(self.json_file):
            make_json(self.json_file)
        else:
            self.file_label_statuses = load_json_if_exists(self.json_file)

        files_n_dir, self.file_entries = get_files_in_dir(directory_chosen, self.ext_allowed, self.file_label_statuses)
        self.amount_of_entries = len(self.file_entries)
        dump_dict_to_json(self.json_file, self.file_label_statuses)

        self.GUI.directory.set(files_n_dir)
        self.GUI.curr_file_name.set(self.file_entries[0])
        self.GUI.file_label_status.set(self.file_label_statuses[self.file_entries[0]])

        # update scrolled text. clear it everytime to accomodate for new files.
        self.GUI.scroll_text.delete('1.0', tkinter.END)
        self.GUI.scroll_text.insert(tkinter.INSERT, self.GUI.directory.get());

    def lower_pos(self):
        # to avoid negative indexing
        if self.current_file_index != 0:
            self.current_file_index -= 1
            self.GUI.curr_file_name.set(self.file_entries[self.current_file_index])
            self.GUI.file_label_status.set(self.file_label_statuses[self.file_entries[self.current_file_index]])

    def incr_pos(self):
        if self.current_file_index != self.amount_of_entries-1:
            self.current_file_index += 1
            self.GUI.curr_file_name.set(self.file_entries[self.current_file_index])
            self.GUI.file_label_status.set(self.file_label_statuses[self.file_entries[self.current_file_index]])
 
    def approve(self):
        '''Decides if the drawn changes will be applied'''
        cv2.imwrite(self.file_entries[self.current_file_index], self.file_being_read)
        # update file status to indicate it has been drawn over
        self.file_label_statuses[self.file_entries[self.current_file_index]] = "True"
        self.GUI.file_label_status.set(self.file_label_statuses[self.file_entries[self.current_file_index]])
        dump_dict_to_json(self.json_file, self.file_label_statuses)

    def reject(self):
        '''Rejects the applied changes and falls back to a backup copy'''
        self.file_being_read = self.backup_file_cpy

        
        set_label = self.file_label_statuses[self.file_entries[self.current_file_index]] = "False"

        self.GUI.file_label_status.set(set_label)
