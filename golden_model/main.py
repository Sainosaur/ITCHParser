from messages import Message

type_dict = {
    "S": 12,   # System Event
    "R": 39,   # Stock Directory
    "H": 25,   # Stock Trading Action
    "Y": 20,   # Reg SHO Restriction
    "L": 26,   # Market Participant Position
    "V": 35,   # MWCB Decline Level
    "W": 12,   # MWCB Status
    "K": 28,   # IPO Quoting Period Update
    "J": 35,   # LULD Auction Collar
    "h": 21,   # Operational Halt
    "A": 36,   # Add Order (no MPID)
    "F": 40,   # Add Order (MPID attribution)
    "E": 31,   # Order Executed
    "C": 36,   # Order Executed with Price
    "X": 23,   # Order Cancel
    "D": 19,   # Order Delete
    "U": 35,   # Order Replace
    "P": 44,   # Trade (non-cross)
    "Q": 40,   # Cross Trade
    "B": 19,   # Broken Trade
    "I": 50,   # NOII
    "N": 20,   # RPII
    "O": 48,   # Direct Listing with Capital Raise
}

def parse(msg_in):
    # Requires a full ITCH 5 message, which is to be parsed fully.
    # 'msg_in' input must be provided as a string to be processed correctly. (Python cannot natively store hexadecimal numbers)
    length_prefix = int(msg_in[0:4], 16) # Extracts length prefix from message
    type = chr(int(msg_in[4:6], 16)) # Extracts type from message and converts into charecter
    if len(msg_in) / 2 != length_prefix:
        return "incompleteMessage"
    try:
        length = type_dict[type]
    except KeyError:
        return "illegalType"
    if length == length_prefix:
        index = 4
        msg = Message()
        msg.set_type(type)
        for field in range(0, len(msg.fields)):
            data = msg_in[index:index + 2*msg.lengths[field]]
            if msg.kinds[field] == "alpha":
                field_entry = ""
                field_index = 0
                for iteration in range(0, msg.lengths[field]):
                    field_entry += chr(int(data[field_index:field_index + 2], 16))
                    field_index += 2
                setattr(msg, msg.fields[field], field_entry)
            else:
                setattr(msg, msg.fields[field], int(data,16))

            index += 2*msg.lengths[field]
        return msg
    else:
        return "lengthMismatch"

decoded_message = parse("002441000100001f1aced9f000000000000000109242000000644141504c202020200001e208")

print(vars(decoded_message))
