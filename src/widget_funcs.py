from pathlib import Path
import os
import cv2
import tkinter

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
        self.file_being_read = -1 # cv2 matrix
        self.backup_file_cpy = -1

    def file_ext_allowed(self, file_str, ext_list):
        '''Checks if file in directory is supported filetype'''
        for ext in ext_list:
            if file_str.endswith(ext):
                return True
            continue

        return False

    def get_files_in_dir(self, directory):
        dir_list = ""
        full_file_paths = []
        
        for d in os.listdir(directory):
            filename = Path(d).name
            
            if not self.file_ext_allowed(filename, self.ext_allowed):
                continue
            
            full_file_directory = os.path.join(directory, d)

            self.file_label_statuses[full_file_directory] = "False"
            full_file_paths.append(full_file_directory)
            dir_list += filename
            dir_list += "\n"

        self.file_entries = full_file_paths
        amount_of_entries = len(full_file_paths)
 
        return dir_list
    
    def mouse_event(self, event, x,y, flags, param):
        '''checks for LMB click'''
        if event == cv2.EVENT_LBUTTONDOWN:
            self.points.append((x,y))

    def draw_square(self):
        self.file_being_read = cv2.imread(self.file_entries[self.current_file_index])
        self.backup_file_cpy = cv2.imread(self.file_entries[self.current_file_index])

        cv2.namedWindow(self.file_entries[self.current_file_index], cv2.WINDOW_NORMAL)
        cv2.imshow(self.file_entries[self.current_file_index], self.file_being_read)

        cv2.setMouseCallback(self.file_entries[self.current_file_index], self.mouse_event)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        cv2.rectangle(self.file_being_read, self.points[0], self.points[1], (0,0,255), 3)

    def preview(self):
        '''preview the drawn image before applying the changes'''
        cv2.namedWindow(self.file_entries[self.current_file_index], cv2.WINDOW_NORMAL)
        cv2.imshow(self.file_entries[self.current_file_index], self.file_being_read)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def choose_file(self):
        directory_chosen = tkinter.filedialog.askdirectory()
        files_n_dir = self.get_files_in_dir(directory_chosen)

        self.GUI.directory.set(files_n_dir)
        self.GUI.curr_file_name.set(self.file_entries[0])
        self.GUI.file_label_status.set(self.file_label_statuses[self.file_entries[0]])

        self.GUI.scroll_text.delete('1.0', tkinter.END)
        self.GUI.scroll_text.insert(tkinter.INSERT, self.GUI.directory.get());

    def lower_pos(self):
        if self.current_file_index != 0:
            self.current_file_index -= 1
            self.GUI.curr_file_name.set(self.file_entries[self.current_file_index])
            self.GUI.file_label_status.set(self.file_label_statuses[self.file_entries[self.current_file_index]])

    def incr_pos(self):
        if self.current_file_index != self.amount_of_entries-1:
            self.current_file_index += 1
            try:
                self.GUI.curr_file_name.set(self.file_entries[self.current_file_index])
                self.GUI.file_label_status.set(self.file_label_statuses[self.file_entries[self.current_file_index]])
            except IndexError:
                pass
 
    def approve(self):
        '''Decides if the drawn changes will be applied'''
        cv2.imwrite(self.file_entries[self.current_file_index], self.file_being_read)
        # update file status to indicate it has been drawn over
        self.file_label_statuses[self.file_entries[self.current_file_index]] = "True"

        self.GUI.file_label_status.set(self.file_label_statuses[self.file_entries[self.current_file_index]])

    def reject(self):
        '''Rejects the applied changes and falls back to a backup copy'''
        self.file_being_read = self.backup_file_cpy
        self.file_label_statuses[self.file_entries[self.current_file_index]] = "False"

        self.GUI.file_label_status.set(self.file_label_statuses[self.file_entries[self.current_file_index]])


