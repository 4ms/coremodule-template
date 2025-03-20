#include "CoreModules/CoreProcessor.hh"
#include "info/MyModule_info.hh"

namespace MetaModule
{

class MyModuleCore : public CoreProcessor {
	using Info = MyModuleInfo;

public:
	MyModuleCore() = default;

	void update(void) override {
		// set outputs based on inputs and parameters

		out = 1.f;
		outL = 2.f;
		outR = 2.f;
	}

	void set_param(int param_id, float val) override {

		switch (param_id) {

			case Info::KnobAttack:
				break;

			case Info::KnobDecay:
				break;

				//etc
		}
	}

	void set_samplerate(float sr) override {
	}

	void set_input(int input_id, float val) override {
		switch (input_id) {

			case Info::InputAttackcv:
				break;

			case Info::InputWavecv:
				break;

				//etc
		}
	}

	float get_output(int output_id) const override {
		switch (output_id) {

			case Info::OutputOut:
				return out;
				break;

			case Info::OutputLout:
				return outL;
				break;

			case Info::OutputRout:
				return outR;
				break;
		}

		return 0;
	}

	void mark_input_unpatched(int input_id) override {
	}

	void mark_input_patched(int input_id) override {
	}

private:
	float out = 0;
	float outL = 0;
	float outR = 0;
};

} // namespace MetaModule
