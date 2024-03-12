import unittest
from MemoryGenerator import MemoryGenerator


class TestMemoryGenerator(unittest.TestCase):
    def test_generate_vhdl_from_memory_content(self):
        memory_generator = MemoryGenerator()

        memory_content = [
            "00000000000000000000000000000001"
        ]


        expected_vhdl_code = """library IEEE;
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
    0 => B"00000000000000000000000000000001",
    others => x"00000000"
    );

begin

Instruction<=rom(conv_integer(PC));
   
end Behavioral;
"""

        generated_vhdl_code = memory_generator.generate_vhdl_from_memory_content(memory_content, "test_output.vhd")

        self.assertEqual(generated_vhdl_code, expected_vhdl_code)


if __name__ == "__main__":
    unittest.main()
