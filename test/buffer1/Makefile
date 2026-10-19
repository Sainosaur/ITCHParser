# Setup to test Buffer1 in isolation


SIM = nvc
TOPLEVEL_LANG = vhdl
VHDL_SOURCES = $(PWD)/../../src/types_pkg.vhd $(PWD)/../../src/buffer1.vhd
COCOTB_TOPLEVEL = buffer1
COCOTB_TEST_MODULES = buffer1
SIM_ARGS += --wave=$(COCOTB_TOPLEVEL).ghw

include $(shell cocotb-config --makefiles)/Makefile.sim
