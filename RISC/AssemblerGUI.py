import tkinter as tk
from tkinter import filedialog, messagebox


class AssemblerGUI:
    def __init__(self, root, controller):
        self.root = root
        self.root.title("Assembler GUI")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        window_width = 600
        window_height = 300
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        self.controller = controller

        self.file_path = tk.StringVar()
        self.output_file_name = tk.StringVar(value="Instruction_Memory.vhd")

        style = {"font": ("Arial", 12)}

        self.label_file = tk.Label(root, text="Select File:", **style)
        self.label_file.pack(pady=10)

        self.file_entry = tk.Entry(root, textvariable=self.file_path, width=40, **style)
        self.file_entry.pack(pady=5)

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file, **style)
        self.browse_button.pack(pady=5)

        self.label_output = tk.Label(root, text="Output File Name:", **style)
        self.label_output.pack(pady=5)

        self.output_entry = tk.Entry(root, textvariable=self.output_file_name, width=40, **style)
        self.output_entry.pack(pady=5)

        self.start_button = tk.Button(root, text="Start", command=self.controller.start_assembling, **style)
        self.start_button.pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.file_path.set(file_path)

    def show_message(self, message):
        tk.messagebox.showinfo("Assembler", message)
