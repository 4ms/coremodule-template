#pragma once
#include "CoreModules/elements/element_info.hh"
#include "helpers/4ms_elements.hh"
#include <array>

namespace MetaModule
{

struct MYMODULEInfo : ModuleInfoBase {
	static constexpr std::string_view slug{"MYMODULE"};
	static constexpr std::string_view description{"Template module that's a dual attenuverter"};
	static constexpr uint32_t width_hp = 4;
	static constexpr std::string_view svg_filename{"res/modules/MyModule.svg"};
	static constexpr std::string_view png_filename{"MyPlugin/modules/MyModule.png"};

	using enum Coords;

	static constexpr std::array<Element, 6> Elements{{
		Knob9mm{{to_mm<72>(28.9), to_mm<72>(46.86), Center, "Level 1", ""}, 1.0f},
		Knob9mm{{to_mm<72>(28.8), to_mm<72>(94.96), Center, "Level 2", ""}, 1.0f},
		AnalogJackInput4ms{{to_mm<72>(28.88), to_mm<72>(168.72), Center, "In 1", ""}},
		AnalogJackInput4ms{{to_mm<72>(28.88), to_mm<72>(216.87), Center, "In 2", ""}},
		AnalogJackOutput4ms{{to_mm<72>(28.88), to_mm<72>(265.02), Center, "Out 1", ""}},
		AnalogJackOutput4ms{{to_mm<72>(28.88), to_mm<72>(313.16), Center, "Out 2", ""}},
	}};

	enum class Elem {
		Level1Knob,
		Level2Knob,
		In1In,
		In2In,
		Out1Out,
		Out2Out,
	};

	enum {
		LevelKnob_1,
		LevelKnob_2,
		NumKnobs,
	};

	enum {
		Input_1,
		Input_2,
		NumInJacks,
	};

	enum {
		Output_1,
		Output_2,
		NumOutJacks,
	};
};

} // namespace MetaModule
