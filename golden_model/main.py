from messages import type_to_length, Message, incompleteMessageError, illegalLengthError



def parse(msg_in):
    # Requires a full ITCH 5 message, which is to be parsed fully.
    # 'msg_in' input must be provided as a string to be processed correctly. (Python cannot natively store hexadecimal numbers)
    length_prefix = int(msg_in[0:4], 16) # Extracts length prefix from message
    type = chr(int(msg_in[4:6], 16)) # Extracts type from message and converts into charecter

    # Error Handling
    if len(msg_in) % 2 != 0:
        raise illegalLengthError
    if (len(msg_in) / 2 - 2) != length_prefix:
        raise incompleteMessageError
    try:
        length = type_to_length[type]
    except KeyError:
        return "illegalType"
    if length != length_prefix:
        return "lengthMismatch"


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

1. 

decoded_message = parse("002441000100001f1aced9f000000000000000109242000000644141504c202020200001e208")

print(vars(decoded_message))
