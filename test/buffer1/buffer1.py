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
async def direct_input_ones_test(dut):
    Clock(dut.clk, 1, "ns").start()

    for i in range(9):
        data_in = [255] * i + [0] * (8-i)
        await FallingEdge(dut.clk)
        await reset(dut)
        dut.direct_data_in.value = data_in
        dut.n_in.value = i

        await RisingEdge(dut.clk)
        await ReadOnly()

        output_data = process_output(dut)
        expected_data = data_in + [0] * 56
        c.log.info(expected_data)
        c.log.info(output_data)
        c.log.info(dut.n_stored.value)
        assert output_data == expected_data
