import cocotb as c
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ReadOnly
from cocotb.clock import Clock
import random as r

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


@c.test
async def direct_input_ones_test(dut):
    Clock(dut.clk, 1, "ns").start()

    for i in range(9):
        data_in = [255] * i + [0] * (8-i)
        await reset(dut)
        dut.direct_data_in.value = data_in
        dut.n_in.value = i

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
        message_length = r.randint(8,16)
        message = []

        for i in range(message_length):
            message.append(r.randint(0,255))
        message = [0] * (16- message_length) + message

        await FallingEdge(dut.clk)
        await reset(dut)

        dut.temp_data_in.value = message[0:8]
        dut.direct_data_in.value = message[8:]
        dut.n_in.value = message_length

        await RisingEdge(dut.clk)
        await ReadOnly()

        output_data = process_output(dut)
        expected_output = message[16 - message_length:]


        assert output_data[0:message_length] == expected_output
        assert dut.n_stored.value == message_length

@c.test
async def full_itch_message_test(dut):
    Clock(dut.clk, 1, "ns").start()
    for n in range(1000):
        starting_message_length = r.randint(14,52) # Create an initial message of starting length
        real_message = []
        flat_message = []
        current_set = []
        current_count = 0
        last_set_count = 0
        for i in range(starting_message_length):
            if current_count < 8:
                random_number = r.randint(0,255)
                current_set.append(random_number)
                flat_message.append(random_number)
                current_count += 1
            else:
                real_message.append(current_set)
                random_number = r.randint(0,255)
                flat_message.append(random_number)
                current_set = [random_number]
                current_count = 1
        last_set_count = len(current_set)
        for i in range(8 - len(current_set)): # Ensures final set is added to message correctly
            current_set.append(0)
        real_message.append(current_set)

        surplus_injection_length = r.randint(0,8) # Add an additional extra message to feed into temp_data_in. Simulating a partial message in ITCH 5
        original_surplus_message = []
        surplus_message = []
        for i in range(8 - surplus_injection_length):
            surplus_message.append(0)
        for i in range(surplus_injection_length):
            random_number = r.randint(0,255)
            original_surplus_message.append(random_number)
            surplus_message.append(random_number)

        await reset(dut)

        dut.direct_data_in.value = real_message[0]
        dut.temp_data_in.value = surplus_message
        dut.n_in.value = 8 + surplus_injection_length

        await RisingEdge(dut.clk)
        await ReadOnly()

        for i in range(1, len(real_message)):
            await FallingEdge(dut.clk)
            dut.direct_data_in.value = real_message[i]
            dut.temp_data_in.value = [0] * 8
            if i == len(real_message) - 1:
                dut.n_in.value = last_set_count
            else:
                dut.n_in.value = 8

            await RisingEdge(dut.clk)
            await ReadOnly()

        expected_output = original_surplus_message + flat_message
        n_stored = dut.n_stored.value
        assert expected_output == process_output(dut)[0:n_stored]
