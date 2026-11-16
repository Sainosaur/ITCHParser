LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.numeric_std.all;



ENTITY type_LUT IS
    PORT (
        clk: IN STD_LOGIC; -- Unused. The LUT is combinational; kept so existing port maps don't change
        message_type: IN STD_LOGIC_VECTOR(7 DOWNTO 0);
        message_length: OUT STD_LOGIC_VECTOR(7 DOWNTO 0)
    );
END type_LUT;


-- Maps an ITCH 5 message type (ASCII) to the total frame length in bytes, including the 2-byte
-- length prefix. Mirrors type_to_length in golden_model/parse.py, plus 2 for every entry.
-- Combinational: message_length follows message_type with no clock delay.
-- An unrecognised type outputs 0, which is never a legal length (the shortest frame is 14),
-- so the caller can treat 0 as "illegalType".
ARCHITECTURE behavioral of type_LUT IS
BEGIN

    message_length <= x"00" WHEN message_type = x"00" ELSE -- No message
                      x"0E" WHEN message_type = x"53" ELSE -- S: System Event (12 + 2)
                      x"29" WHEN message_type = x"52" ELSE -- R: Stock Directory (39 + 2)
                      x"1B" WHEN message_type = x"48" ELSE -- H: Stock Trading Action (25 + 2)
                      x"16" WHEN message_type = x"59" ELSE -- Y: Reg SHO Restriction (20 + 2)
                      x"1C" WHEN message_type = x"4C" ELSE -- L: Market Participant Position (26 + 2)
                      x"25" WHEN message_type = x"56" ELSE -- V: MWCB Decline Level (35 + 2)
                      x"0E" WHEN message_type = x"57" ELSE -- W: MWCB Status (12 + 2)
                      x"1E" WHEN message_type = x"4B" ELSE -- K: IPO Quoting Period Update (28 + 2)
                      x"25" WHEN message_type = x"4A" ELSE -- J: LULD Auction Collar (35 + 2)
                      x"17" WHEN message_type = x"68" ELSE -- h: Operational Halt (21 + 2)
                      x"26" WHEN message_type = x"41" ELSE -- A: Add Order, no MPID (36 + 2)
                      x"2A" WHEN message_type = x"46" ELSE -- F: Add Order, MPID attribution (40 + 2)
                      x"21" WHEN message_type = x"45" ELSE -- E: Order Executed (31 + 2)
                      x"26" WHEN message_type = x"43" ELSE -- C: Order Executed with Price (36 + 2)
                      x"19" WHEN message_type = x"58" ELSE -- X: Order Cancel (23 + 2)
                      x"15" WHEN message_type = x"44" ELSE -- D: Order Delete (19 + 2)
                      x"25" WHEN message_type = x"55" ELSE -- U: Order Replace (35 + 2)
                      x"2E" WHEN message_type = x"50" ELSE -- P: Trade, non-cross (44 + 2)
                      x"2A" WHEN message_type = x"51" ELSE -- Q: Cross Trade (40 + 2)
                      x"15" WHEN message_type = x"42" ELSE -- B: Broken Trade (19 + 2)
                      x"34" WHEN message_type = x"49" ELSE -- I: NOII (50 + 2)
                      x"16" WHEN message_type = x"4E" ELSE -- N: RPII (20 + 2)
                      x"32" WHEN message_type = x"4F" ELSE -- O: Direct Listing with Capital Raise (48 + 2)
                      x"00";

END ARCHITECTURE behavioral;
