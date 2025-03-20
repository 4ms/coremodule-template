#include "core/MyModule2.hh"
#include "info/MyModule2_info.hh"
#include "vcv/generic_module.hh"

using namespace MetaModule;

rack::Model *modelMyModule2 = GenericModule<MyModule2Info, MyModule2>::create();
