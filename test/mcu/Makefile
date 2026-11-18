# Setup to test MCU along all constituent components


SIM = nvc
TOPLEVEL_LANG = vhdl
VHDL_SOURCES = $(PWD)/../../src/types_pkg.vhd $(PWD)/../../src/buffer1.vhd $(PWD)/../../src/buffer0.vhd $(PWD)/../../src/type_LUT.vhd $(PWD)/../../src/mcu.vhd
COCOTB_TOPLEVEL = mcu
COCOTB_TEST_MODULES = mcu
SIM_ARGS += --wave=$(COCOTB_TOPLEVEL).ghw
export PYTHONPATH := $(abspath ../..):$(PYTHONPATH)

include $(shell cocotb-config --makefiles)/Makefile.sim
