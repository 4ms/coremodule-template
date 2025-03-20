#pragma once
#include "CoreModules/elements/element_info.hh"
#include "helpers/4ms_elements.hh"

#include <array>

namespace MetaModule
{
struct MyModule2Info : ModuleInfoBase {
	static constexpr std::string_view slug{"MyModule2"};
	static constexpr std::string_view description{"My Module Full Name"};
	static constexpr uint32_t width_hp = 8;
	static constexpr std::string_view svg_filename{"res/modules/MyModule2.svg"};
	static constexpr std::string_view png_filename{"4ms/MyModule2.png"};

	using enum Coords;

	static constexpr std::array<Element, 12> Elements{{
		Davies1900hBlackKnob{{to_mm<72>(31.73), to_mm<72>(47.84), Center, "Attack", ""}, 0.5f},
		Davies1900hBlackKnob{{to_mm<72>(83.37), to_mm<72>(47.84), Center, "Decay", ""}, 0.5f},
		Davies1900hBlackKnob{{to_mm<72>(31.83), to_mm<72>(104.81), Center, "Wave", ""}, 0.0f},
		Davies1900hBlackKnob{{to_mm<72>(83.37), to_mm<72>(104.81), Center, "Mix", ""}, 0.0f},
		AnalogJackInput4ms{{to_mm<72>(31.97), to_mm<72>(167.24), Center, "AttackCV", ""}},
		AnalogJackInput4ms{{to_mm<72>(83.51), to_mm<72>(167.24), Center, "Decay CV", ""}},
		AnalogJackInput4ms{{to_mm<72>(31.97), to_mm<72>(214.44), Center, "WaveCV", ""}},
		AnalogJackInput4ms{{to_mm<72>(83.51), to_mm<72>(214.44), Center, "MixCV", ""}},
		AnalogJackInput4ms{{to_mm<72>(31.97), to_mm<72>(263.51), Center, "Gate", ""}},
		AnalogJackOutput4ms{{to_mm<72>(83.51), to_mm<72>(263.54), Center, "Out", ""}},
		AnalogJackOutput4ms{{to_mm<72>(31.97), to_mm<72>(311.1), Center, "LOut", ""}},
		AnalogJackOutput4ms{{to_mm<72>(83.51), to_mm<72>(311.13), Center, "ROut", ""}},
	}};

	enum class Elem {
		AttackKnob,
		DecayKnob,
		WaveKnob,
		MixKnob,
		AttackcvIn,
		DecayCvIn,
		WavecvIn,
		MixcvIn,
		GateIn,
		Out,
		LoutOut,
		RoutOut,
	};

	// Legacy naming (safe to remove once all legacy 4ms CoreModules are converted)

	enum {
		KnobAttack,
		KnobDecay,
		KnobWave,
		KnobMix,
		NumKnobs,
	};

	enum {
		InputAttackcv,
		InputDecay_Cv,
		InputWavecv,
		InputMixcv,
		InputGate,
		NumInJacks,
	};

	enum {
		OutputOut,
		OutputLout,
		OutputRout,
		NumOutJacks,
	};
};
} // namespace MetaModule
