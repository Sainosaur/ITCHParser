LIBRARY ieee;
USE ieee.std_logic_1164.all;


PACKAGE types_pkg IS
    -- The standard data input port used across the design
    TYPE ITCH_DATA_ARRAY IS ARRAY(7 DOWNTO 0) OF STD_LOGIC_VECTOR(7 DOWNTO 0);
    -- The standard buffer1 storage and output architecture. Usable for ports and registers for buffer1
    TYPE BUFFER1_ARRAY IS ARRAY(0 TO 63) OF STD_LOGIC_VECTOR(7 DOWNTO 0);
END types_pkg;
