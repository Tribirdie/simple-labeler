import tkinter
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext

class GUI:
    def __init__(self, mediator, wf):
        self.mediator = mediator
        self.wf = wf
        self.binded_keys = {
                "Up": self.wf.lower_pos,
                "w": self.wf.lower_pos,
                "W": self.wf.lower_pos,
                "Down": self.wf.incr_pos, 
                "s": self.wf.incr_pos,
                "S": self.wf.incr_pos,
                "p": self.wf.preview,
                "P": self.wf.preview,
                "d": self.wf.draw_square,
                "D": self.wf.draw_square,
                "a": self.wf.approve,
                "A": self.wf.approve,
                "r": self.wf.reject,
                "R": self.wf.reject,
                "q": self.wf.choose_file,
                "Q": self.wf.choose_file
        }

    def binding_func(self, event):
        self.binded_keys[event.keysym]()

    def main(self):
        # keys for switching files in dir
        self.mediator.gui.bind("<Up>", self.binding_func)
        self.mediator.gui.bind("<Down>", self.binding_func)

        self.mediator.gui.bind("w", self.binding_func)
        self.mediator.gui.bind("W", self.binding_func)
        self.mediator.gui.bind("s", self.binding_func)
        self.mediator.gui.bind("S", self.binding_func)
        # shortcut for preview
        self.mediator.gui.bind("p", self.binding_func) 
        self.mediator.gui.bind("P", self.binding_func)
        # shortcut for draw
        self.mediator.gui.bind("d", self.binding_func)
        self.mediator.gui.bind("D", self.binding_func)
        # shortcut for approve
        self.mediator.gui.bind("a", self.binding_func)
        self.mediator.gui.bind("A", self.binding_func)
        # shortcut for reject
        self.mediator.gui.bind("r", self.binding_func)
        self.mediator.gui.bind("R", self.binding_func)
        # shortcut for choose directory
        self.mediator.gui.bind("q", self.binding_func)
        self.mediator.gui.bind("Q", self.binding_func)

        tkinter.Label(self.mediator.gui, textvariable=self.mediator.req("curr_file", "gui")).place(x=170, y=10)
        tkinter.Entry(self.mediator.gui, textvariable=self.mediator.req("filename", "gui")).place(width=400, x=280, y=10)
        tkinter.Button(self.mediator.gui, text="Preview", command=self.wf.preview).place(width=200, x=280, y=35)
        tkinter.Button(self.mediator.gui, text="Approve", command=self.wf.approve).place(width=100, x=480, y=35)
        tkinter.Button(self.mediator.gui, text="Reject", command=self.wf.reject).place(width=100, x=580, y=35)

        tkinter.Label(self.mediator.gui, textvariable=self.mediator.req("curr_label", "gui")).place(x=170, y=100)
        tkinter.Entry(self.mediator.gui, textvariable=self.mediator.req("label", "gui")).place(x=280, y=100)

        tkinter.Label(self.mediator.gui, textvariable=self.mediator.req("curr_folder_label", "gui")).place(x=170, y=130)
        tkinter.Entry(self.mediator.gui, textvariable=self.mediator.req("curr_folder", "gui")).place(width=300, x=265, y=130)

        ttk.Separator(self.mediator.gui, orient="horizontal").place(height=1, width=710, x=0, y=320)
        ttk.Button(self.mediator.gui, text="Directory", command=self.wf.choose_file).place(height=150, x=10, y=330)
        ttk.Button(self.mediator.gui, text="Draw", command=self.wf.draw_square).place(height=150, width=300, x=100, y=330)

        ttk.Button(self.mediator.gui, text="Up", command=self.wf.lower_pos).place(height=75, width=275, x=405, y=330)
        ttk.Button(self.mediator.gui, text="Down", command=self.wf.incr_pos).place(height=70, width=275, x=405, y=410)

        self.mediator.gui.mainloop()
