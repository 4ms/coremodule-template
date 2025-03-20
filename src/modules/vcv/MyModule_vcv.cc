#include "core/MyModule.hh"
#include "info/MyModule_info.hh"
#include "vcv/generic_module.hh"

using namespace MetaModule;

rack::Model *modelMyModule = GenericModule<MyModuleInfo, MyModule>::create();
