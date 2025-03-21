#include "plugin-vcv.hh"
#include "vcv/generic_module.hh"

#include "core/MyModule.hh"
#include "core/MyModule2.hh"

using namespace MetaModule;

rack::Plugin *pluginInstance;

void init(rack::Plugin *p) {
	pluginInstance = p;

	rack::Model *modelMyModule = GenericModule<MyModuleInfo, MyModule>::create();
	rack::Model *modelMyModule2 = GenericModule<MyModule2Info, MyModule2>::create();

	p->addModel(modelMyModule);
	p->addModel(modelMyModule2);
}
