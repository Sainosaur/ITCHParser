LIBRARY ieee;
USE ieee.std_logic_1164.all;


PACKAGE types_pkg IS
    -- The standard data input port used across the design
    TYPE ITCH_DATA_PORT IS ARRAY(7 DOWNTO 0) OF STD_LOGIC_VECTOR(7 DOWNTO 0);
END types_pkg;
