LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.numeric_std.all;
USE work.types_pkg.all;


ENTITY buffer1 IS
    PORT (
        clk: IN STD_LOGIC;
        direct_data_in: IN ITCH_DATA_ARRAY;
        temp_data_in: IN ITCH_DATA_ARRAY;
        direct_n_in: IN INTEGER RANGE 0 to 8;
        temp_n_in: IN INTEGER RANGE 0 to 8;
        reset: IN STD_LOGIC;
        n_stored: OUT INTEGER RANGE 0 to 64;
        data_out: OUT BUFFER1_ARRAY
    );
END buffer1;


ARCHITECTURE behavioral OF buffer1 IS
    SIGNAL data_registers : BUFFER1_ARRAY := (OTHERS => "00000000");
    SIGNAL n_stored_register : INTEGER RANGE 0 to 64 := 0;
    SIGNAL first_messsge : STD_LOGIC := '1';
BEGIN
    n_stored <= n_stored_register;
    data_out <= data_registers;

    PROCESS (clk)
    BEGIN
        IF rising_edge(clk) THEN
            IF reset = '1' THEN
                n_stored_register <= direct_n_in + temp_n_in;
                FOR i IN 0 TO 7 LOOP
                    IF (temp_n_in) > i THEN
                        data_registers(i) <= temp_data_in(temp_n_in - 1 - i);
                    END IF;
                END LOOP;
                FOR i IN 0 TO 7 LOOP
                    data_registers(temp_n_in + i) <= direct_data_in(7 - i);
                END LOOP;
            ELSE
                n_stored_register <= n_stored_register + direct_n_in;
                FOR i IN 0 TO 7 LOOP
                    data_registers(n_stored_register + i) <= direct_data_in(7 - i);
                END LOOP;
            END IF;
        END IF;
    END PROCESS;

END ARCHITECTURE behavioral;
