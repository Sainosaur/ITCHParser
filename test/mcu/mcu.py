import cocotb as c
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ReadOnly
from cocotb.clock import Clock
from golden_model import parse
import random as r



MESSAGES = [
    ("S", [0, 12, 83, 159, 119, 65, 101, 45, 228, 189, 229, 192, 153, 67]),  # 'S', 14 bytes
    ("R", [0, 39, 82, 241, 69, 215, 110, 67, 216, 236, 29, 125, 160, 65, 65, 80, 76, 32, 32, 32, 32, 86, 83, 0, 0, 0, 100, 89, 73, 80, 32, 84, 89, 78, 32, 89, 0, 0, 0, 3, 89]),  # 'R', 41 bytes
    ("H", [0, 25, 72, 3, 92, 187, 47, 52, 62, 55, 123, 154, 162, 83, 80, 89, 32, 32, 32, 32, 32, 80, 32, 77, 87, 67, 49]),  # 'H', 27 bytes
    ("Y", [0, 20, 89, 40, 220, 195, 14, 9, 53, 204, 17, 211, 87, 78, 86, 68, 65, 32, 32, 32, 32, 50]),  # 'Y', 22 bytes
    ("L", [0, 26, 76, 158, 18, 113, 225, 16, 237, 32, 111, 92, 102, 71, 83, 67, 79, 65, 65, 80, 76, 32, 32, 32, 32, 89, 80, 65]),  # 'L', 28 bytes
    ("V", [0, 35, 86, 223, 87, 42, 159, 40, 37, 74, 15, 231, 93, 0, 0, 0, 82, 207, 136, 35, 242, 0, 0, 0, 82, 138, 50, 161, 23, 0, 0, 0, 81, 13, 209, 38, 43]),  # 'V', 37 bytes
    ("W", [0, 12, 87, 247, 113, 247, 17, 49, 13, 228, 204, 65, 50, 50]),  # 'W', 14 bytes
    ("K", [0, 28, 75, 5, 134, 92, 119, 21, 62, 106, 55, 83, 145, 78, 86, 68, 65, 32, 32, 32, 32, 0, 0, 160, 84, 65, 0, 44, 0, 213]),  # 'K', 30 bytes
    ("J", [0, 35, 74, 77, 38, 209, 66, 75, 6, 154, 101, 106, 175, 65, 65, 80, 76, 32, 32, 32, 32, 0, 44, 198, 212, 0, 9, 250, 12, 0, 41, 51, 83, 0, 0, 0, 6]),  # 'J', 37 bytes
    ("h", [0, 21, 104, 209, 139, 78, 91, 23, 166, 80, 215, 209, 63, 90, 86, 90, 90, 84, 32, 32, 32, 66, 72]),  # 'h', 23 bytes
    ("A", [0, 36, 65, 14, 152, 65, 150, 45, 199, 191, 242, 145, 1, 103, 127, 209, 57, 216, 74, 29, 59, 66, 0, 0, 17, 146, 65, 77, 68, 32, 32, 32, 32, 32, 0, 48, 101, 194]),  # 'A', 38 bytes
    ("F", [0, 40, 70, 96, 90, 148, 26, 1, 41, 215, 91, 30, 36, 11, 246, 78, 247, 115, 236, 40, 209, 66, 0, 0, 6, 74, 77, 83, 70, 84, 32, 32, 32, 32, 0, 33, 6, 101, 86, 73, 82, 84]),  # 'F', 42 bytes
    ("E", [0, 31, 69, 88, 42, 131, 51, 32, 29, 134, 82, 219, 208, 118, 125, 82, 116, 198, 141, 235, 94, 0, 0, 3, 118, 191, 151, 3, 192, 150, 250, 187, 124]),  # 'E', 33 bytes
    ("C", [0, 36, 67, 199, 239, 204, 24, 4, 176, 75, 189, 187, 1, 242, 31, 245, 235, 110, 215, 143, 94, 0, 0, 2, 235, 87, 58, 197, 154, 53, 95, 42, 245, 78, 0, 20, 126, 179]),  # 'C', 38 bytes
    ("X", [0, 23, 88, 87, 8, 70, 147, 11, 201, 139, 142, 143, 78, 175, 155, 116, 248, 79, 252, 191, 67, 0, 0, 10, 36]),  # 'X', 25 bytes
    ("D", [0, 19, 68, 78, 98, 45, 112, 10, 2, 204, 124, 109, 129, 38, 28, 55, 75, 160, 118, 87, 215]),  # 'D', 21 bytes
    ("U", [0, 35, 85, 184, 157, 176, 110, 20, 172, 123, 217, 232, 161, 12, 109, 234, 61, 184, 90, 92, 211, 252, 152, 80, 0, 20, 185, 173, 182, 0, 0, 19, 57, 0, 69, 209, 92]),  # 'U', 37 bytes
    ("P", [0, 44, 80, 236, 114, 103, 233, 30, 97, 8, 37, 199, 204, 152, 13, 198, 255, 189, 149, 61, 195, 83, 0, 0, 8, 2, 90, 86, 90, 90, 84, 32, 32, 32, 0, 55, 130, 196, 14, 66, 212, 60, 37, 71, 241, 157]),  # 'P', 46 bytes
    ("Q", [0, 40, 81, 250, 164, 234, 132, 4, 48, 163, 105, 57, 239, 0, 0, 0, 0, 0, 12, 212, 2, 90, 86, 90, 90, 84, 32, 32, 32, 0, 44, 77, 53, 53, 1, 224, 136, 214, 163, 77, 63, 67]),  # 'Q', 42 bytes
    ("B", [0, 19, 66, 251, 55, 187, 79, 13, 166, 105, 240, 68, 30, 111, 63, 2, 64, 43, 55, 216, 24]),  # 'B', 21 bytes
    ("I", [0, 50, 73, 95, 125, 38, 53, 37, 188, 107, 175, 113, 215, 0, 0, 0, 0, 0, 1, 33, 146, 0, 0, 0, 0, 0, 0, 232, 3, 83, 81, 81, 81, 32, 32, 32, 32, 32, 0, 59, 148, 57, 0, 64, 2, 158, 0, 42, 49, 23, 67, 52]),  # 'I', 52 bytes
    ("N", [0, 20, 78, 74, 129, 120, 88, 14, 104, 37, 129, 112, 249, 65, 77, 68, 32, 32, 32, 32, 32, 83]),  # 'N', 22 bytes
]


async def reset(dut):
    await FallingEdge(dut.clk)
    dut.reset.value = 1
    await RisingEdge(dut.clk)
    dut.reset.value = 0


def process_output(dut):
    data_out = []
    for value in dut.data_out.value:
        data_out.append(value.integer) # Extracts values from cocotb LogicArray
    return data_out


# @c.test
async def continous_itch_stream_test(dut):
    Clock(dut.clk, 1, "ns").start()
    dut.reset.value = 0

    stream = []
    message_types = []
    current_index = 0
    check_index = 0
    type_index = -1

    for n in range(10):
        message_type = r.randint(0,21)
        type, message = MESSAGES[message_type]
        stream += message
        message_types.append(type)
    while current_index < len(stream):
        await FallingEdge(dut.clk)
        dut.ITCH_stream.value = stream[current_index:current_index + 8]
        current_index += 8
        await RisingEdge(dut.clk)
        if current_index >= check_index:
            type_index += 1
            check_index += parse.type_to_length[message_types[type_index]]
            c.log.info(dut.output_ready)
            c.log.info()
            c.log.info(process_output(dut))



@c.test
async def single_itch_test(dut):
    Clock(dut.clk, 1, "ns").start()
    for n in range(10):
        message_index = r.randint(0,21)
        type, message = MESSAGES[message_index]
        await reset(dut)
        for m in range(len(message) % 8 ):
            message.append(0)
        for l in range(int(len(message) / 8)):
            await FallingEdge(dut.clk)
            dut.ITCH_stream.value = message[l*8:(l+1)*8]
            await RisingEdge(dut.clk)
        c.log.info(message)
        c.log.info(process_output(dut))
