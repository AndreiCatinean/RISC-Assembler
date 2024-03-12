class MemoryGenerator:
    def generate_vhdl_from_memory_content(self, memory_content, output_file_name="Instruction_Memory.vhd"):
        """
        Generează codul VHDL pentru o memorie de program care contine formatul binar al unor instructiuni și îl scrie într-un fișier.

        Args:
        memory_content (list): Lista de valori binare reprezentând conținutul memoriei.
        output_file_name (str): Numele fișierului VHDL de ieșire. Implicit este "Instruction_Memory.vhd".

        Returns:
        str: Codul VHDL generat.
        """
        vhdl_code = f"""library IEEE;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use IEEE.STD_LOGIC_1164.ALL;

entity Instruction_Memory is
    Port ( 
        PC : in STD_LOGIC_VECTOR (7 downto 0);
        Instruction : out STD_LOGIC_VECTOR (31 downto 0));
end Instruction_Memory;

architecture Behavioral of Instruction_Memory is

type rom_mem is array(0 to 255) of std_logic_vector(31 downto 0);
signal rom: rom_mem:=(
"""
        for index, value in enumerate(memory_content):
            vhdl_code += f"    {index} => B\"{value}\",\n"

        vhdl_code += """    others => x"00000000"
    );

begin

Instruction<=rom(conv_integer(PC));
   
end Behavioral;
"""

        with open(output_file_name, "w") as vhdl_file:
            vhdl_file.write(vhdl_code)

        return vhdl_code
