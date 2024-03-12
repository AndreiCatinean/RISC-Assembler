class Parser:

    def parse_file(self, text_file):
        """
        Parsază conținutul unui fișier de asamblare și returnează o listă de coduri binare pentru fiecare instrucțiune.

        Args:
        text_file (str): Calea către fișierul de asamblare.

        Returns:
        list: O listă de coduri binare pentru fiecare instrucțiune de asamblare.
        """
        binary_codes = []
        line_nr = 1
        with open(text_file, 'r') as file:
            for line in file:
                binary_codes.append(self.parse_instruction(line.strip(), line_nr))
                line_nr = line_nr + 1

        return binary_codes

    def parse_instruction(self, instruction, line):
        """
        Parsază o singură instrucțiune de asamblare și returnează reprezentarea sa binară.

        Args:
        instruction (str): Instrucțiunea de asamblare.
        line (int): Numărul liniei în fișierul de input.

        Returns:
        str: Reprezentarea binară a instrucțiunii de asamblare.
        """
        binary_code = ""

        opcodes = {
            'NOP': '00000000',
            'MOVA': '01000000',
            'ADD': '00000010',
            'SUB': '00000101',
            'AND': '00001000',
            'OR': '00001001',
            'XOR': '00001010',
            'NOT': '00001011',
            'ADDI': '00100010',
            'SUBI': '00100101',
            'ANDI': '00101000',
            'ORI': '00101001',
            'XORI': '00101010',
            'ADDU': '01000010',
            'SUBU': '01000101',
            'MOVB': '00001100',
            'SHR': '00001101',
            'SHL': '00001110',
            'LD': '00010000',
            'ST': '00100000',
            'JMPR': '01110000',
            'SGTE': '01110101',
            'SLT': '01100101',
            'BZ': '01100000',
            'BNZ': '01010000',
            'JMP': '01101000',
            'JMPL': '00110000',
            'HALT': '01101001'
        }

        instruction = instruction.replace(',', ' ')
        parts = instruction.split()

        opcode = opcodes.get(parts[0])
        if opcode is None:
            raise ValueError(f"Invalid operation: {parts[0]} at line {str(line)}")

        try:
            self.validate_instruction_format(parts[0], len(parts) - 1)

            if parts[0] in {'NOP', 'HALT'}:
                binary_code = opcode + '000000000000000000000000'
            elif parts[0] in {'MOVA', 'NOT', 'LD'}:
                binary_code = opcode + self.register_to_binary(parts[1]) + self.register_to_binary(
                    parts[2]) + '0000000000000000'
            elif parts[0] in {'MOVB'}:
                binary_code = opcode + self.register_to_binary(parts[1]) + '0000' + self.register_to_binary(
                    parts[2]) + '000000000000'
            elif parts[0] in {'ST'}:
                binary_code = opcode + '0000' + self.register_to_binary(parts[1]) + self.register_to_binary(
                    parts[2]) + '000000000000'
            elif parts[0] in {'ADD', 'SUB', 'AND', 'OR', 'XOR', 'SGTE', 'SLT'}:
                binary_code = opcode + self.register_to_binary(parts[1]) + self.register_to_binary(
                    parts[2]) + self.register_to_binary(parts[3]) + '000000000000'
            elif parts[0] in {'ADDI', 'SUBI', 'ANDI', 'ORI', 'XORI'}:
                binary_code = opcode + self.register_to_binary(parts[1]) + self.register_to_binary(
                    parts[2]) + self.immediate_to_binary(parts[3])
            elif parts[0] in {'ADDU', 'SUBU', 'SHR', 'SHL'}:
                binary_code = opcode + self.register_to_binary(parts[1]) + self.register_to_binary(
                    parts[2]) + self.immediate_to_binary(parts[3], True)
            elif parts[0] in {'JMPR'}:
                binary_code = opcode + '0000' + self.register_to_binary(parts[1]) + '0000000000000000'
            elif parts[0] in {'BZ', 'BNZ'}:
                binary_code = opcode + '0000' + self.register_to_binary(parts[1]) + self.immediate_to_binary(parts[2])
            elif parts[0] in {'JMP'}:
                binary_code = opcode + '00000000' + self.immediate_to_binary(parts[1])
            elif parts[0] in {'JMPL'}:
                binary_code = opcode + self.register_to_binary(parts[1]) + '0000' + self.immediate_to_binary(parts[2])


            return binary_code
        except Exception as e:
            raise ValueError(f"Error: {e}. Line {str(line)}")


    def register_to_binary(self, register):
        """
        Convertește un nume de registru în reprezentarea sa binară.

        Args:
        register (str): Numele registrului în formatul 'Rx' unde x este un număr între 0 și 15.

        Returns:
        str: Reprezentarea binară a registrului.
        """
        if not register.startswith("R") or not register[1:].isdigit():
            raise ValueError("Invalid register format. Use format 'Rx' where x is a number between 0 and 15.")

        register_number = int(register[1:])

        if not (0 <= register_number <= 15):
            raise ValueError("Invalid register number. Use a number between 0 and 15.")

        return format(register_number, '04b')

    def immediate_to_binary(self, immediate, unsigned=False):
        """
        Convertește o valoare imediată (integer / binar / hexa) în reprezentarea sa binară.

        Args:
        immediate (str): Valoarea imediată în diverse formate.
        unsigned (bool): Dacă este True, tratează valoarea imediată ca fiind fara semn.

        Returns:
        str: Reprezentarea binară a valorii imediate.
        """
        if immediate.startswith("B'") and immediate.endswith("'"):
            binary_value = immediate[2:-1]
            if not all(bit in "01" for bit in binary_value) or len(binary_value) > 16:
                raise ValueError("Invalid binary value. Use a valid binary format (e.g., b'001').")
            immediate = int(binary_value, 2)
        elif immediate.startswith("X'") and immediate.endswith("'"):
            hex_value = immediate[2:-1]
            if not all(c in "0123456789ABCDEF" for c in hex_value) or len(hex_value) > 4:
                raise ValueError("Invalid hexadecimal value. Use a valid hexadecimal format (e.g., x'FFFF').")
            immediate = int(hex_value, 16)
        else:
            try:
                immediate = int(immediate)
            except ValueError:
                raise ValueError(
                    "Invalid immediate value. Use an integer, binary (e.g., b'001'), or hexadecimal (e.g., x'FFFF').")
            if unsigned and immediate < 0:
                raise ValueError("Unsigned immediate value must be non-negative")
        value = immediate & 0xFFFF
        return format(value, '016b')

    def validate_instruction_format(self, instruction_name, num_operands):
        """
        Validează formatul instrucțiunii în funcție de numărul așteptat de operanzi.

        Args:
        instruction_name (str): Numele instrucțiunii de asamblare.
        num_operands (int): Numărul real de operanzi.
        """
        expected_operands = {
            'NOP': 0,
            'MOVA': 2,
            'ADD': 3,
            'SUB': 3,
            'AND': 3,
            'OR': 3,
            'XOR': 3,
            'NOT': 2,
            'ADDI': 3,
            'SUBI': 3,
            'ANDI': 3,
            'ORI': 3,
            'XORI': 3,
            'ADDU': 3,
            'SUBU': 3,
            'MOVB': 2,
            'SHR': 3,
            'SHL': 3,
            'LD': 2,
            'ST': 2,
            'JMPR': 1,
            'SGTE': 3,
            'SLT': 3,
            'BZ': 2,
            'BNZ': 2,
            'JMP': 1,
            'JMPL': 2,
            'HALT': 0
        }

        expected_count = expected_operands.get(instruction_name)
        if expected_count is None or num_operands != expected_count:
            raise ValueError(f"Invalid number or format of operands for {instruction_name} ")
