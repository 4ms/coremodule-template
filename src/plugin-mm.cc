#include "CoreModules/register_module.hh"
#include "core/MyModule.hh"
#include "core/MyModule2.hh"

void init() {
	using namespace MetaModule;

	std::string_view brand = "MyPlugin";

	register_module<MyModule, MyModuleInfo>(brand);
	register_module<MyModule2, MyModule2Info>(brand);
}
