#include "plugin.hh"

rack::Plugin *pluginInstance;

__attribute__((__visibility__("default"))) void init(rack::Plugin *p) {
	pluginInstance = p;

	p->addModel(modelMyModule);
}
