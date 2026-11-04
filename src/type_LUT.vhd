LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.numeric_std.all;



ENTITY type_LUT IS
    PORT (
        clk: IN STD_LOGIC;
        message_type: IN STD_LOGIC_VECTOR(7 DOWNTO 0);
        message_length: OUT STD_LOGIC_VECTOR(7 DOWNTO 0)
    );
END type_LUT;


-- Maps an ITCH 5 message type (ASCII) to the total frame length in bytes, including the 2-byte
-- length prefix. Mirrors type_to_length in golden_model/parse.py, plus 2 for every entry.
-- An unrecognised type outputs 0, which is never a legal length (the shortest frame is 14),
-- so the caller can treat 0 as "illegalType".
ARCHITECTURE behavioral of type_LUT IS
BEGIN

    PROCESS(clk)
    BEGIN
        IF rising_edge(clk) THEN
            CASE message_type IS
                WHEN x"00" => message_length <= x"00"; -- Serves as option to reset
                WHEN x"53" => message_length <= x"0E"; -- S: System Event (12 + 2)
                WHEN x"52" => message_length <= x"29"; -- R: Stock Directory (39 + 2)
                WHEN x"48" => message_length <= x"1B"; -- H: Stock Trading Action (25 + 2)
                WHEN x"59" => message_length <= x"16"; -- Y: Reg SHO Restriction (20 + 2)
                WHEN x"4C" => message_length <= x"1C"; -- L: Market Participant Position (26 + 2)
                WHEN x"56" => message_length <= x"25"; -- V: MWCB Decline Level (35 + 2)
                WHEN x"57" => message_length <= x"0E"; -- W: MWCB Status (12 + 2)
                WHEN x"4B" => message_length <= x"1E"; -- K: IPO Quoting Period Update (28 + 2)
                WHEN x"4A" => message_length <= x"25"; -- J: LULD Auction Collar (35 + 2)
                WHEN x"68" => message_length <= x"17"; -- h: Operational Halt (21 + 2)
                WHEN x"41" => message_length <= x"26"; -- A: Add Order, no MPID (36 + 2)
                WHEN x"46" => message_length <= x"2A"; -- F: Add Order, MPID attribution (40 + 2)
                WHEN x"45" => message_length <= x"21"; -- E: Order Executed (31 + 2)
                WHEN x"43" => message_length <= x"26"; -- C: Order Executed with Price (36 + 2)
                WHEN x"58" => message_length <= x"19"; -- X: Order Cancel (23 + 2)
                WHEN x"44" => message_length <= x"15"; -- D: Order Delete (19 + 2)
                WHEN x"55" => message_length <= x"25"; -- U: Order Replace (35 + 2)
                WHEN x"50" => message_length <= x"2E"; -- P: Trade, non-cross (44 + 2)
                WHEN x"51" => message_length <= x"2A"; -- Q: Cross Trade (40 + 2)
                WHEN x"42" => message_length <= x"15"; -- B: Broken Trade (19 + 2)
                WHEN x"49" => message_length <= x"34"; -- I: NOII (50 + 2)
                WHEN x"4E" => message_length <= x"16"; -- N: RPII (20 + 2)
                WHEN x"4F" => message_length <= x"32"; -- O: Direct Listing with Capital Raise (48 + 2)
                WHEN OTHERS => message_length <= (OTHERS => '0');
            END CASE;
        END IF;
    END PROCESS;
END ARCHITECTURE behavioral;
