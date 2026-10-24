import cocotb as c
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ReadOnly
from cocotb.clock import Clock
import random as r

async def reset(dut):
    await FallingEdge(dut.clk)
    dut.direct_n_in.value = 0
    dut.temp_n_in.value = 0
    dut.reset.value = 1
    await RisingEdge(dut.clk)
    dut.reset.value = 0

def process_output(dut):
    data_out = []
    for value in dut.data_out.value:
        data_out.append(value.integer) # Extracts values from cocotb LogicArray
    return data_out


@c.test
async def direct_input_ones_test(dut):
    Clock(dut.clk, 1, "ns").start()
    dut.temp_n_in.value = 0
    for i in range(9):
        data_in = [255] * i + [0] * (8-i)
        await reset(dut)
        dut.direct_data_in.value = data_in
        dut.direct_n_in.value = i

        await RisingEdge(dut.clk)
        await ReadOnly()

        output_data = process_output(dut)
        expected_data = data_in + [0] * 56

        assert output_data == expected_data
        assert dut.n_stored.value == i

@c.test
async def random_split_message_injection(dut):
    Clock(dut.clk, 1, "ns").start()
    for n in range(1000):
        direct_length = r.randint(0,8)
        temp_length = r.randint(0,8)
        direct_message = []
        temp_message = []

        for i in range(direct_length):
            direct_message.append(r.randint(0,255))
        direct_message = direct_message + [0] * (8 - direct_length)

        for i in range(temp_length):
            temp_message.append(r.randint(0,255))
        temp_message =  [0] * (8 - temp_length) + temp_message

        await reset(dut)

        dut.reset.value = 1
        dut.temp_n_in.value = temp_length
        dut.temp_data_in.value = temp_message
        dut.direct_data_in.value = direct_message
        dut.direct_n_in.value = direct_length

        await RisingEdge(dut.clk)
        await ReadOnly()

        output_data = process_output(dut)
        expected_output = temp_message[8 - temp_length:] + direct_message[0:direct_length]


        assert output_data[0:temp_length + direct_length] == expected_output
        assert dut.n_stored.value == temp_length + direct_length

@c.test
async def full_itch_message_test(dut):
    Clock(dut.clk, 1, "ns").start()
    for n in range(1000):
        message_length = r.randint(14,52) # Create an initial message of starting length
        temp_message_length = r.randint(0,8) # Moves a component of the message out into a temp injection

        direct_message_length = message_length - temp_message_length
        message = []
        flat_message = []
        current_set = []
        current_count = 0
        last_set_count = 0
        for i in range(direct_message_length):
            if current_count < 8:
                random_number = r.randint(0,255)
                current_set.append(random_number)
                flat_message.append(random_number)
                current_count += 1
            else:
                message.append(current_set)
                random_number = r.randint(0,255)
                flat_message.append(random_number)
                current_set = [random_number]
                current_count = 1
        last_set_count = len(current_set)
        for i in range(8 - len(current_set)): # Ensures final set is added to message correctly
            current_set.append(0)
        message.append(current_set)

        temp_message = []
        for i in range(8 - temp_message_length):
            temp_message.append(0)
        for i in range(temp_message_length):
            random_number = r.randint(0,255)
            temp_message.append(random_number)

        await FallingEdge(dut.clk)

        dut.reset.value = 1
        dut.direct_data_in.value = message[0]
        dut.temp_data_in.value = temp_message
        dut.temp_n_in.value = temp_message_length
        dut.direct_n_in.value = min(len(message[0]), len(flat_message))

        await RisingEdge(dut.clk)
        await ReadOnly()


        for i in range(1, len(message)):
            await FallingEdge(dut.clk)
            dut.temp_n_in.value = 0
            dut.reset.value = 0
            dut.direct_data_in.value = message[i]
            dut.temp_data_in.value = [0] * 8

            if i == len(message) - 1:
                dut.direct_n_in.value = last_set_count
            else:
                dut.direct_n_in.value = 8

            await RisingEdge(dut.clk)
            await ReadOnly()

        expected_output = temp_message[8 - temp_message_length:] + flat_message
        n_stored = dut.n_stored.value

        assert expected_output == process_output(dut)[0:n_stored]
