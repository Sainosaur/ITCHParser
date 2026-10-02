LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.numeric_std.all;
USE work.types_pkg.all;

ENTITY buffer0 IS
    PORT (
        clk : in STD_LOGIC;
        data_in: in ITCH_DATA_ARRAY;
        n_in : in UNSIGNED(2 DOWNTO 0);
        read_enable: in STD_LOGIC;
        write_enable : in STD_LOGIC;
        reset: in STD_LOGIC;
        data_out : out ITCH_DATA_ARRAY;
        n_stored: out UNSIGNED(2 DOWNTO 0)
    );
END buffer0;


ARCHITECTURE behavioral OF buffer0 IS
    SIGNAL data_registers : ITCH_DATA_ARRAY := (OTHERS => "00000000");
    SIGNAL n_stored_register : UNSIGNED(2 DOWNTO 0) := (OTHERS => '0');
BEGIN
    n_stored <= n_stored_register;
    PROCESS(clk)
    BEGIN
        IF rising_edge(clk) THEN
            IF reset THEN
                FOR i IN 0 TO 7 LOOP
                    data_registers(i) <= "00000000";
                    n_stored_register <= (OTHERS => '0');
                END LOOP;
            ELSIF read_enable THEN
                data_registers <= data_in;
                n_stored_register <= n_in;
            ELSIF write_enable THEN
                FOR i IN 0 TO 7 LOOP
                    IF i < n_stored_register THEN
                        data_out(i) <= data_registers(i);
                    ELSE
                        data_out(i) <= (OTHERS => '0');
                    END IF;
                END LOOP;
            END IF;
        END IF;
    END PROCESS;

END behavioral;
