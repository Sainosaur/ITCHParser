LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.numeric_std.all;

ENTITY buffer0 IS
    PORT (
        clk : in STD_LOGIC;
        data_in_0 : in STD_LOGIC_VECTOR(7 DOWNTO 0);
        data_in_1 : in STD_LOGIC_VECTOR(7 DOWNTO 0);
        data_in_2 : in STD_LOGIC_VECTOR(7 DOWNTO 0);
        data_in_3 : in STD_LOGIC_VECTOR(7 DOWNTO 0);
        data_in_4 : in STD_LOGIC_VECTOR(7 DOWNTO 0);
        data_in_5 : in STD_LOGIC_VECTOR(7 DOWNTO 0);
        data_in_6 : in STD_LOGIC_VECTOR(7 DOWNTO 0);
        data_in_7 : in STD_LOGIC_VECTOR(7 DOWNTO 0);
        n_in : in STD_LOGIC_VECTOR(3 DOWNTO 0);
        read_enable: in STD_LOGIC;
        write_enable : in STD_LOGIC;
        reset: in STD_LOGIC;
        data_out_0 : in STD_LOGIC_VECTOR(7 DOWNTO 0);
        data_out_1 : in STD_LOGIC_VECTOR(7 DOWNTO 0);
        data_out_2 : in STD_LOGIC_VECTOR(7 DOWNTO 0);
        data_out_3 : in STD_LOGIC_VECTOR(7 DOWNTO 0);
        data_out_4 : in STD_LOGIC_VECTOR(7 DOWNTO 0);
        data_out_5 : in STD_LOGIC_VECTOR(7 DOWNTO 0);
        data_out_6 : in STD_LOGIC_VECTOR(7 DOWNTO 0);
        data_out_7 : in STD_LOGIC_VECTOR(7 DOWNTO 0);
        n_stored: out STD_LOGIC
    );
END buffer0;


ARCHITECTURE behavioral OF buffer0 IS

BEGIN
    PROCESS(clk)
    BEGIN

    END PROCESS;

END behavioral;
