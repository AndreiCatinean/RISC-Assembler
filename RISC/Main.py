import tkinter as tk
from AssemblerGUI import AssemblerGUI
from AssemblerController import AssemblerController


def main():
    root = tk.Tk()
    controller = AssemblerController()
    gui = AssemblerGUI(root, controller)
    controller.set_gui(gui)
    root.mainloop()


if __name__ == "__main__":
    main()
