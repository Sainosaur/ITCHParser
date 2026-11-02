import cocotb as c
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ReadOnly
from cocotb.clock import Clock



@c.test
async def basic_test():
    return 1
