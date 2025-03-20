#include "CoreModules/CoreProcessor.h"
#include "info/Slug_info.hh"

namespace MetaModule
{

class SlugCore : public CoreProcessor {
	using Info = SlugInfo;

public:
	SlugCore() = default;

	void update() override {
	}

	void set_param(int param_id, float val) override {
	}

	void set_input(int input_id, float val) override {
	}

	float get_output(int output_id) const override {
		return 0.f;
	}

	void set_samplerate(float sr) override {
	}

	float get_led_brightness(int led_id) const override {
		return 0.f;
	}

	void mark_input_unpatched(int input_id) override {
	}

	void mark_input_patched(int input_id) override {
	}

};

} // namespace MetaModule
