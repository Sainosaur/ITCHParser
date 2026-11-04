LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.numeric_std.all;
USE work.types_pkg.all;


ENTITY mcu IS
    PORT (
        clk : IN STD_LOGIC;
        ITCH_stream : IN ITCH_DATA_ARRAY;
        reset: IN STD_LOGIC;
        message_type: OUT STD_LOGIC_VECTOR(7 DOWNTO 0);
        output_ready: OUT STD_LOGIC;
        err_out: OUT STD_LOGIC;
        data_out : OUT BUFFER1_ARRAY -- Temporary testing output. Will be replaced by OCU once it's built
    );
END mcu;


ARCHITECTURE behavioral OF mcu IS
    SIGNAL message_type_register : STD_LOGIC_VECTOR(7 DOWNTO 0) := (OTHERS => '0');
    SIGNAL current_length : INTEGER RANGE 0 TO 64 := 0;
    SIGNAL LUT_length: STD_LOGIC_VECTOR(7 DOWNTO 0) := (OTHERS => '0');
    SIGNAL header_message_length : INTEGER RANGE 0 TO 64 := 0;

    SIGNAL temp_data_in : ITCH_DATA_ARRAY := (OTHERS => "00000000");
    SIGNAL direct_n_in : INTEGER RANGE 0 TO 8 := 0;
    SIGNAL temp_n_in : INTEGER RANGE 0 TO 8 := 0;
    SIGNAL b0_n_in : INTEGER RANGE 0 TO 8 := 0;
    SIGNAL b0_reset : STD_LOGIC := '0';
    SIGNAL b1_reset: STD_LOGIC := '0';
    SIGNAL b1_n_stored: INTEGER RANGE 0 to 64;
    SIGNAL b0_write_enable: STD_LOGIC := '0';
    SIGNAL reset_next_cycle: STD_LOGIC := '0';

BEGIN
    type_LUT : ENTITY work.type_LUT(behavioral) PORT MAP(clk => clk, message_type => message_type_register, message_length => LUT_length);
    buffer1: ENTITY work.buffer1(behavioral) PORT MAP (
        clk => clk,
        direct_data_in => ITCH_stream,
        temp_data_in => temp_data_in,
        direct_n_in => direct_n_in,
        temp_n_in => temp_n_in,
        reset => b1_reset,
        n_stored => b1_n_stored,
        data_out => data_out
    );
    buffer0: ENTITY work.buffer0(behavioral) PORT MAP (
      clk => clk,
      data_in => ITCH_stream,
      n_in => b0_n_in,
      write_enable => b0_write_enable,
      reset => b0_reset,
      data_out => temp_data_in,
      n_stored => temp_n_in
    );

    message_type <= message_type_register;
    err_out <= '1' WHEN b1_n_stored /= current_length OR TO_INTEGER(UNSIGNED(LUT_length)) /= header_message_length ELSE '0';

    PROCESS(clk)
    BEGIN
        IF rising_edge(clk) THEN
            IF reset = '1' THEN
                message_type_register <= (OTHERS => '0');
                current_length <= 0;
                header_message_length <= 0;
                direct_n_in <= 0;
                b0_n_in <= 0;
                b0_reset <= '1';
                b0_write_enable <= '0';
                reset_next_cycle <= '1';
            ELSE
                b1_reset <= reset_next_cycle;
                FOR i in 1 TO 8 LOOP
                    IF current_length + i = header_message_length + 1 THEN
                        header_message_length <= TO_INTEGER(UNSIGNED(ITCH_stream(7 - i))) + 2;
                    ELSIF current_length + i = header_message_length + 2 THEN
                        message_type_register <= ITCH_stream(7 - i);
                    END IF;
                END LOOP;
                IF current_length + 8 > header_message_length THEN
                    current_length <= 8 - header_message_length + current_length;
                    direct_n_in <= header_message_length - current_length;
                    b0_n_in <= 8 - header_message_length + current_length;
                    b0_write_enable <= '1';
                    output_ready <= '1';
                    reset_next_cycle <= '1';
                ELSE
                    current_length <= current_length + 8;
                    b0_n_in <= 0;
                    direct_n_in <= 8;
                    b0_write_enable <= '0';
                    output_ready <= '0';
                    reset_next_cycle <= '0';
                END IF;
            END IF;
        END IF;
    END PROCESS;


END ARCHITECTURE behavioral;
