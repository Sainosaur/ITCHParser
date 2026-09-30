LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.numeric_std.all;


ENTITY buffer0 IS
    PORT (
        clk : IN STD_LOGIC;
        data_in: IN STD_LOGIC_VECTOR(63 DOWNTO 0);
        n_next: IN INTEGER RANGE 0 to 15;
        data_out: OUT STD_LOGIC_VECTOR(127 DOWNTO 0);
        n_active: OUT INTEGER RANGE 0 to 15
    );
END buffer0;


ARCHITECTURE behavioral OF buffer0 IS
    TYPE memory IS ARRAY (15 DOWNTO 0) OF STD_LOGIC_VECTOR(7 DOWNTO 0);
    SIGNAL data : memory := (OTHERS => "00000000");
    SIGNAL data_out_register : memory := (OTHERS => "00000000");
    SIGNAL slots_available: INTEGER RANGE 0 to 15 := 15;
BEGIN
    -- Connects the data output registers to the relevant bytes of output ports.
    data_out(127 DOWNTO 120) <= data_out_register(0);
    data_out(119 DOWNTO 112) <= data_out_register(1);
    data_out(111 DOWNTO 104) <= data_out_register(2);
    data_out(103 DOWNTO 96)  <= data_out_register(3);
    data_out(95 DOWNTO 88)   <= data_out_register(4);
    data_out(87 DOWNTO 80)   <= data_out_register(5);
    data_out(79 DOWNTO 72)   <= data_out_register(6);
    data_out(71 DOWNTO 64)   <= data_out_register(7);
    data_out(63 DOWNTO 56)   <= data_out_register(8);
    data_out(55 DOWNTO 48)   <= data_out_register(9);
    data_out(47 DOWNTO 40)   <= data_out_register(10);
    data_out(39 DOWNTO 32)   <= data_out_register(11);
    data_out(31 DOWNTO 24)   <= data_out_register(12);
    data_out(23 DOWNTO 16)   <= data_out_register(13);
    data_out(15 DOWNTO 8)    <= data_out_register(14);
    data_out(7 DOWNTO 0)     <= data_out_register(15);

    PROCESS(clk)
    BEGIN
        IF rising_edge(clk) THEN
            FOR i IN 0 to 7 LOOP
                data(slots_available - i) <= data_in(63 - i*8 DOWNTO 56 - i*8);
            END LOOP;
            FOR i IN 0 to n_next - 1 LOOP
                data_out_register(15 - i) <= data(15 - i);
            END LOOP;
            FOR i IN n_next DOWNTO 0 LOOP
                data_out_register(i) <= (OTHERS => '0');
            END LOOP;
            FOR i IN 15 - n_next DOWNTO 0 LOOP
                data(i + n_next) <= data(i);
            END LOOP;
            FOR i IN 0 TO n_next LOOP
                data(i) <= "00000000";
            END LOOP;
            slots_available <= slots_available + n_next - 8;
            n_active <= n_next;
        END IF;
    END PROCESS;
END behavioral;
