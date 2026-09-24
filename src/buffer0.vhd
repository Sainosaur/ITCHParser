LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.numeric_std.all;


ENTITY buffer0 IS
    PORT (
        clk : IN STD_LOGIC;
        data_in: IN STD_LOGIC_VECTOR(63 DOWNTO 0);
        n_out: IN STD_LOGIC_VECTOR(3 DOWNTO 0);
        data_out: OUT STD_LOGIC_VECTOR(127 DOWNTO 0);
        n_active: OUT STD_LOGIC_VECTOR(3 DOWNTO 0)
    );
END buffer0;


ARCHITECTURE behavioral OF buffer0 IS
BEGIN

END behavioral;
