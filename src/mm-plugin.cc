#include "CoreModules/register_module.hh"

__attribute__((__visibility__("default"))) void init() {
	MetaModule::register_module<SimpleGain>("NativeExample", "SimpleGain", info, "NativeExample/simple_gain.png");
}
