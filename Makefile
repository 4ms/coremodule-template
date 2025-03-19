RACK_DIR ?= ../..
METAMODULE_SDK_DIR ?= ../metamodule-plugin-sdk

SOURCES =
SOURCES += $(wildcard src/modules/core/*.cc)
SOURCES += $(wildcard src/modules/core/*.cpp)

SOURCES += $(wildcard src/vcv/modules/*.cc)
SOURCES += src/vcv/comm_module.cc
SOURCES += src/plugin.cc

DISTRIBUTABLES += $(wildcard LICENSE*) res

MMBUILD_DIR = build-mm

mm: metamodule

$(MMBUILD_DIR):
	@mkdir -p $(MMBUILD_DIR)

config: $(MMBUILD_DIR)
	cmake --fresh -B $(MMBUILD_DIR) -G Ninja -DMETAMODULE_SDK_DIR=$(METAMODULE_SDK_DIR)

metamodule: $(MMBUILD_DIR)
	cmake --build $(MMBUILD_DIR)
	

.PHONY: mm metamodule config

include $(RACK_DIR)/plugin.mk
