'''GUI for the FileVisual program.'''

from src.gui import GUI
from src.widget_funcs import WidgetFunctions
from src.shared_data import Comms

def main():
    med = Comms()
    logic = WidgetFunctions(med)
    gui_loop = GUI()
    gui_loop.main(med, logic)

if __name__ == "__main__":
    main()
