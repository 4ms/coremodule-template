#include "core/MYMODULE.hh"
#include "info/MYMODULE_info.hh"
#include "vcv/generic_module.hh"

using namespace MetaModule;

rack::Model *modelMYMODULE = GenericModule<MYMODULEInfo, MYMODULECore>::create();
