import cocotb as c
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ReadOnly
from cocotb.clock import Clock
import random as r


async def reset(dut):
    dut.reset.value = 1
    await RisingEdge(dut.clk)
    dut.reset.value = 0

def process_output(dut):
    data_out = []
    for value in dut.data_out.value:
        data_out.append(value.integer) # Extracts values from cocotb LogicArray
    return data_out


@c.test
async def reset_operation_test(dut):
# Writes data and a mask to the system and attempts to 'reset' the system.
# Tests the reset routine of the system to ensure it actually resets the system correctly.

    Clock(dut.clk, 1, "ns").start()
    data_in = [255, 255, 255, 255, 255, 255, 255, 255]
    n_in = 8

    await reset(dut)

    dut.write_enable.value = 1
    dut.data_in.value = data_in
    dut.n_in.value = n_in

    await RisingEdge(dut.clk)
    await ReadOnly()
    assert process_output(dut) == data_in

    await FallingEdge(dut.clk)
    dut.write_enable.value = 0

    await reset(dut)
    await ReadOnly()

    assert process_output(dut) == [0] * 8
    assert dut.n_stored.value == 0


@c.test
async def mask_test(dut):
    # Tests if system can effectively cut out outputs that shouldn't be given out and
    # checks if n_stored is given out correctly. Tests system's ability to read inputs

    n_in = 8
    data_in = [255, 255, 255, 255, 255, 255, 255, 255]
    Clock(dut.clk, 1, "ns").start()
    # Resets DUT
    await reset(dut)
    dut.write_enable.value = 1
    dut.data_in.value = data_in
    dut.n_in.value = n_in
    await RisingEdge(dut.clk)

    while n_in != -1:
        await FallingEdge(dut.clk)
        dut.n_in.value = n_in
        await RisingEdge(dut.clk)
        await ReadOnly()
        data_out = process_output(dut)
        assert data_out == data_in
        assert dut.n_stored.value == n_in
        n_in -= 1
        data_in = [0] + data_in[0:7]

@c.test
async def random_input_test(dut):
# Exposes system to 1000 randomly generated test inputs each with a different output
# mask. Tests the system's ability to read and output different values with different mask
    Clock(dut.clk, 1, "ns").start()
    for n in range(1000):
        data_in = []
        n_in = r.randint(0,8)
        for i in range(8):
            data_in.append(r.randint(0, 255))

        await FallingEdge(dut.clk)

        dut.write_enable.value = 1
        dut.data_in.value = data_in
        dut.n_in.value = n_in

        await RisingEdge(dut.clk)
        await ReadOnly()

        data_out = process_output(dut)
        data_expected = [0] * (8 - n_in) + data_in[8-n_in:]
        assert dut.n_stored.value == n_in
        assert data_out == data_expected


@c.test
async def hold_write_test(dut):
# Sets the value of write_enable to zero after some data is assigned to the input
# of the register itself. Tests to ensure the system can hold data when it's not being
# written to.
    data_in = [0, 1, 255, 29, 219, 212, 128, 92]
    Clock(dut.clk, 1, "ns").start()
    await reset(dut)
    dut.write_enable.value = 1
    dut.data_in.value = data_in
    dut.n_in.value = 8

    await RisingEdge(dut.clk)
    await ReadOnly()



    await FallingEdge(dut.clk)
    dut.write_enable.value = 0
    dut.data_in.value = [0] * 8

    await RisingEdge(dut.clk)
    await Timer(5, "ns") # Waits for 5 full clock cycles

    assert process_output(dut) == data_in
