RACK_DIR ?= ../..
METAMODULE_SDK_DIR ?= metamodule-plugin-sdk

SOURCES =
SOURCES += $(wildcard src/vcv/modules/*.cc)
SOURCES += src/vcv/comm_module.cc
SOURCES += src/plugin.cc

INCLUDES = -Isrc \
		   -Isrc/modules \
		   -I$(METAMODULE_SDK_DIR)/metamodule-core-interface \
		   -I$(METAMODULE_SDK_DIR)/cpputil

FLAGS += $(INCLUDES) -std=c++20

DISTRIBUTABLES += $(wildcard LICENSE*) res

MMBUILD_DIR = build

mm: metamodule

$(MMBUILD_DIR):
	@mkdir -p $(MMBUILD_DIR)

config: $(MMBUILD_DIR)
	cmake --fresh -B $(MMBUILD_DIR) -G Ninja -DMETAMODULE_SDK_DIR=$(METAMODULE_SDK_DIR)

metamodule: $(MMBUILD_DIR)
	cmake --build $(MMBUILD_DIR)
	

.PHONY: mm metamodule config

include $(RACK_DIR)/plugin.mk
