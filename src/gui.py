import tkinter
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext

class GUI:
    def __init__(self):
        pass

    def main(self, mediator, wf):
        tkinter.Label(mediator.gui, textvariable=mediator.req("curr_file", "gui")).place(x=170, y=10)
        tkinter.Entry(mediator.gui, textvariable=mediator.req("filename", "gui")).place(width=400, x=280, y=10)
        tkinter.Button(mediator.gui, text="Preview", command=wf.preview).place(width=200, x=280, y=35)
        tkinter.Button(mediator.gui, text="Approve", command=wf.approve).place(width=100, x=480, y=35)
        tkinter.Button(mediator.gui, text="Reject", command=wf.reject).place(width=100, x=580, y=35)

        tkinter.Label(mediator.gui, textvariable=mediator.req("curr_label", "gui")).place(x=170, y=100)
        tkinter.Entry(mediator.gui, textvariable=mediator.req("label", "gui")).place(x=300, y=100)

        ttk.Separator(mediator.gui, orient="horizontal").place(height=1, width=710, x=0, y=320)
        ttk.Button(mediator.gui, text="Directory", command=wf.choose_file).place(height=150, x=10, y=330)
        ttk.Button(mediator.gui, text="Draw", command=wf.draw_square).place(height=150, width=300, x=100, y=330)
        ttk.Button(mediator.gui, text="Up", command=wf.lower_pos).place(height=75, width=275, x=405, y=330)
        ttk.Button(mediator.gui, text="Down", command=wf.incr_pos).place(height=70, width=275, x=405, y=410)

        mediator.gui.mainloop()
