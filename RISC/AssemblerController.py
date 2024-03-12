from Parser import Parser
from MemoryGenerator import MemoryGenerator


class AssemblerController:
    def __init__(self):
        self.gui = None

    def set_gui(self, gui):
        self.gui = gui

    def start_assembling(self):
        """
        Inițiază procesul de asamblare, utilizând parserul și generatorul de memorie.

        """
        file_path = self.gui.file_path.get()
        output_file_name = self.gui.output_file_name.get()
        try:
            self.remove_blank_lines(file_path)
            if file_path:
                parser = Parser()
                memory_generator = MemoryGenerator()
                binary_codes = parser.parse_file(file_path)
                memory_generator.generate_vhdl_from_memory_content(binary_codes, output_file_name)

                self.gui.show_message("Assembling completed.")
        except Exception as e:
            self.gui.show_message(f"Error during assembling: {str(e)}")

    def remove_blank_lines(self, file_path):
        """
        Elimină liniile goale din fișierul specificat.

        Args:
        file_path (str): Calea către fișierul din care se elimină liniile goale.


        """
        with open(file_path, 'r') as file:
            lines = file.readlines()

        non_blank_lines = [line.strip().upper() for line in lines if line.strip()]

        with open(file_path, 'w') as file:
            file.write('\n'.join(non_blank_lines) + '\n')
