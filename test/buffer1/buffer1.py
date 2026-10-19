import cocotb as c
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ReadOnly
from cocotb.clock import Clock
import random as r

async def reset(dut):
    dut.reset.value = 1
    await RisingEdge(dut.clk)
    dut.reset.value = 0

@c.test
async def direct_input_test(dut):
    Clock(dut.clk, 1, "ns").start()
    data_in = [255] * 8

    for i in range(8):
        await reset(dut)
        await FallingEdge(dut.clk)
        dut.direct_data_in.value = data_in
        dut.n_in.value = 8 - i

        await RisingEdge(dut.clk)
        await ReadOnly()
