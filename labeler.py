'''GUI for the FileVisual program.'''

from src.gui import GUI
from src.widget_funcs import WidgetFunctions

def main():
    gui_loop = GUI()
    logic = WidgetFunctions(gui_loop)
    gui_loop.main(logic)

if __name__ == "__main__":
    main()
