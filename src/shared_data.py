import tkinter
from tkinter import scrolledtext

class Comms:
    def __init__(self):
        self.gui = tkinter.Tk()
        self.gui.resizable(0, 0)
        self.gui.title("File to Image")
        self.set_size_and_pos = self.gui.geometry("710x500+200+200")

        self.directory = tkinter.StringVar(value="")
        self.current_file_label = tkinter.StringVar(value="current file: ")
        self.curr_file_label_status = tkinter.StringVar(value="was file labeled: ")
        self.curr_folder_label = tkinter.StringVar(value="current folder: ")

        self.curr_file_name = tkinter.StringVar(value="")
        self.file_label_status = tkinter.StringVar(value="")
        self.curr_folder = tkinter.StringVar(value="")
        self.directory = tkinter.StringVar(value="")

        self.scroll_text = scrolledtext.ScrolledText(self.gui, wrap='none')
        self.scroll_text.place(width=150, height=300, x=10, y=10)

        self.menu_items_gui = {"curr_file": self.current_file_label,
                "filename": self.curr_file_name, 
                "label": self.file_label_status, 
                "curr_label": self.curr_file_label_status,
                "curr_folder_label": self.curr_folder_label,
                "curr_folder": self.curr_folder
                }

    def req(self, order, sender):
        if sender == "gui":
            return self.menu_items_gui[order]

