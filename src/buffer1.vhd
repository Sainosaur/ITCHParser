LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.numeric_std.all;
USE work.types_pkg.all;


ENTITY buffer1 IS
    PORT (
        clk: IN STD_LOGIC;
        direct_data_in: IN ITCH_DATA_ARRAY;
        temp_data_in: IN ITCH_DATA_ARRAY;
        n_in: IN INTEGER RANGE 0 to 16;
        reset: IN STD_LOGIC;
        n_stored: OUT INTEGER RANGE 0 to 64;
        data_out: OUT BUFFER1_ARRAY
    );
END buffer1;


ARCHITECTURE behavioral OF buffer1 IS
    SIGNAL data_registers : BUFFER1_ARRAY := (OTHERS => "00000000");
    SIGNAL n_stored_register : INTEGER RANGE 0 to 64 := 0;
BEGIN
    n_stored <= n_stored_register;
    data_out <= data_registers;
    PROCESS (clk)
    BEGIN
        IF rising_edge(clk) THEN
            IF reset = '1' THEN
                n_stored_register <= 0;
            ELSE
                n_stored_register <= n_stored_register + n_in;
                FOR i IN 0 TO 7 LOOP
                    IF (n_in - 8) > i THEN
                        data_registers(n_stored_register + i) <= temp_data_in(n_in - 9 - i);
                    END IF;
                END LOOP;
                FOR i IN 0 TO 7 LOOP
                    IF (n_in > 8) THEN
                        data_registers(n_stored_register + n_in - 8 + i) <= direct_data_in(7 - i);
                    ELSE
                        data_registers(n_stored_register + i) <= direct_data_in(7 - i);
                    END IF;
                END LOOP;
            END IF;
        END IF;
    END PROCESS;

END ARCHITECTURE behavioral;
