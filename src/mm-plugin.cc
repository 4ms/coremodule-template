#include "CoreModules/register_module.hh"
#include "core/MYMODULE.hh"

extern "C" __attribute__((__visibility__("default"))) void init() {
	using namespace MetaModule;

	register_module<MYMODULECore, MYMODULEInfo>("MyPlugin");
}
