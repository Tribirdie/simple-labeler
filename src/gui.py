import tkinter
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from widget_funcs import WidgetFunctions

class GUI:
    def __init__(self):
        self.gui = tkinter.Tk()
        self.gui.resizable(0, 0)
        self.gui.title("File to Image")
        self.set_size_and_pos = self.gui.geometry("710x500+200+200")

        self.directory = tkinter.StringVar(value="")
        self.current_file_label = tkinter.StringVar(value="current folder: ")
        self.curr_file_label_status = tkinter.StringVar(value="current file status: ")

        self.curr_file_name = tkinter.StringVar(value="")
        self.file_label_status = tkinter.StringVar(value="")
        self.directory = tkinter.StringVar(value="")

        self.scroll_text = scrolledtext.ScrolledText(self.gui, wrap='none')
        self.scroll_text.place(width=150, height=300, x=10, y=10)

    def main(self, funcs):
        tkinter.Label(self.gui, textvariable=self.current_file_label).place(x=170, y=10)
        tkinter.Entry(self.gui, textvariable=self.curr_file_name).place(width=400, x=280, y=10)
        tkinter.Button(self.gui, text="Preview", command=funcs.preview).place(width=200, x=280, y=35)
        tkinter.Button(self.gui, text="Approve", command=funcs.approve).place(width=100, x=480, y=35)
        tkinter.Button(self.gui, text="Reject", command=funcs.reject).place(width=100, x=580, y=35)

        tkinter.Label(self.gui, textvariable=self.curr_file_label_status).place(x=170, y=100)
        tkinter.Entry(self.gui, textvariable=self.file_label_status).place(x=300, y=100)

        ttk.Separator(self.gui, orient="horizontal").place(height=1, width=710, x=0, y=320)
        ttk.Button(self.gui, text="Directory", command=funcs.choose_file).place(height=150, x=10, y=330)
        ttk.Button(self.gui, text="Draw", command=funcs.draw_square).place(height=150, width=300, x=100, y=330)
        ttk.Button(self.gui, text="Up", command=funcs.lower_pos).place(height=75, width=275, x=405, y=330)
        ttk.Button(self.gui, text="Down", command=funcs.incr_pos).place(height=70, width=275, x=405, y=410)

        self.gui.mainloop()

m = GUI()
s = WidgetFunctions(m)
m.main(s)
