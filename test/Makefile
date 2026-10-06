# Currently being set up to test Buffer0 in isolation


SIM = nvc
TOPLEVEL_LANG = vhdl
VHDL_SOURCES = $(PWD)/../src/types_pkg.vhd $(PWD)/../src/buffer0.vhd
COCOTB_TOPLEVEL = buffer0
COCOTB_TEST_MODULES = buffer0
SIM_ARGS += --wave=$(COCOTB_TOPLEVEL).ghw

include $(shell cocotb-config --makefiles)/Makefile.sim
