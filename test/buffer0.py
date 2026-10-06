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

    while n_in != 0:
        await FallingEdge(dut.clk)
        dut.n_in.value = n_in
        await RisingEdge(dut.clk)
        await ReadOnly()
        c.log.info(dut.n_stored)
        c.log.info(n_in)
        data_out = process_output(dut)
        c.log.info(data_out)
        assert data_out == data_in
        assert dut.n_stored.value == n_in
        n_in -= 1
        data_in = [0] + data_in[0:7]

@c.test
async def random_input_test(dut):
    data_in = []
    for i in range(8):
        data_in.append(r.randint(0, 255))

    Clock(dut.clk, 1, "ns").start()
    # Resets DUT before test
    await reset(dut)
    dut.write_enable.value = 1
    dut.data_in.value = data_in
    dut.n_in.value = 8

    await RisingEdge(dut.clk)
    await ReadOnly()

    data_out = process_output(dut)

    assert data_out == data_in
