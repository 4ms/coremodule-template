#pragma once
#include "CoreModules/SmartCoreProcessor.hh"
#include "info/MyModule2_info.hh"

namespace MetaModule
{

class MyModule2 : public SmartCoreProcessor<MyModule2Info> {
	using Info = MyModule2Info;
	using enum Info::Elem;

public:
	MyModule2() = default;

	void update() override {

		// How to use SmartCoreProcessor:
		//
		// First, look at the _info.hh file. The `enum class Elem` is the list of elements.
		// Use those names to interact with the elements:

		// Get a parameter value:
		// For switches, the return value is an integer referring to the switch position #
		// For buttons, the return value will be MomentaryButton::RELEASED or MomentaryButton::PRESSED
		// For everything else, it's a float
		float wave_knob = getState<WaveKnob>(); // 0..1

		// Get an input jack value (in volts, usually -10V to +10V)
		// The ".value_or(XX)" is the normalization voltage, which is what
		// you get if the jack is not patched
		float wave_cv_volts = getInput<WavecvIn>().value_or(0.f);

		// Set an output in volts:
		setOutput<Out>(2.5f);

		// Set an LED brightness (0..1)
		// setLED<GateLight>(0.5f);
		// For RGB, pass an array of the values:
		// setLED<FullcolorLight>({0.1f, 0.7f, 0.3f});

		////////////////////////////////////////////////////

		// Here's a short tutorial on how to check if a jack is patched or not
		// Example: call isPatched to see if a jack is patched
		if (isPatched<GateIn>()) {

			if (getInput<GateIn>() > 2.5f) {
				setOutput<Out>(5.f);
			} else {
				setOutput<Out>(-5.f);
			}

		} else {
			setOutput<Out>(0.f);
		}

		// Another way is to check if getInput returns a nullopt:

		auto knob = getState<AttackKnob>();
		auto cv = getInput<AttackcvIn>();

		float combined;
		if (cv.has_value()) {
			combined = cv.value() + (knob * 5.f);
		} else {
			combined = knob * 10.f;
		}

		// Another way is to set an unpatched value:
		// Here, DecayCV takes the value of R-Out when MixCV is unpatched

		auto decaycv = getInput<DecayCvIn>().value_or(getOutput<RoutOut>());

		// Can check for outputs being patched, too

		float left_out = combined;								 // pretend these are interesting signals we calculated!
		float right_out = decaycv * (wave_knob + wave_cv_volts); //

		if (isPatched<RoutOut>()) {
			setOutput<LoutOut>(left_out);
			setOutput<RoutOut>(right_out);
		} else {
			setOutput<LoutOut>((left_out + right_out) / 2.f);
		}
	}

	void set_samplerate(float sr) override {
	}
};

} // namespace MetaModule
