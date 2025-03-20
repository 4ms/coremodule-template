import os
import xml.etree.ElementTree
from helpers.xml_helper import register_all_namespaces
from helpers.util import *
from helpers.svg_parse_helpers import *

def createInfoFile(svgFilename, infoFilePath = None, brand = "4ms"):
    if infoFilePath == None:
        infoFilePath = os.getenv('METAMODULE_INFO_DIR')
        if infoFilePath is None:
            infoFilePath = input_default("Directory to save ModuleInfo file", pathFromHere("src/modules/info"))

    if os.path.isdir(infoFilePath) == False:
        # Try infoFilePath as a path relative to the dir containing svgFilename
        svgdir = os.path.dirname(svgFilename)
        infoFilePath = os.path.normpath(os.path.join(svgdir,infoFilePath))
        if os.path.isdir(infoFilePath) == False:
            Log(f"Not a directory: {infoFilePath}. Aborting without creating an info file.")
            return

    if os.path.isfile(svgFilename) == False:
        Log(f"Not a file: {svgFilename}. Aborting without creating an info file.")
        return

    register_all_namespaces(svgFilename)
    tree = xml.etree.ElementTree.parse(svgFilename)
    components = panel_to_components(tree)
    infoFileText = components_to_infofile(components, brand)
    infoFileName = os.path.join(infoFilePath, components['slug']+"_info.hh")
    with open(infoFileName, "w") as f:
        f.write(infoFileText)
        Log(f"Wrote info file: {infoFileName}")
    
    return components['slug']


def panel_to_components(tree):

    components = {}
    #TODO: extract knob long name and description (or is that to be done manually?)
    #.... maybe SVG id = "ShortName#LongName" or "ShortName"
    #.... and description is in some help file

    root = tree.getroot()

    # Deduce DPI and HP:
    components['dpi'] = deduce_dpi(root)
    components['HP'] = round(get_dim_inches(root.get('width')) / 0.2)
    Log(f"HP deduced as {components['HP']}")

    components_group = get_components_group(root)
    components['slug'], components['ModuleName'] = find_slug_and_modulename(components_group)

    if components['slug'] == "Unnamed":
        Log("WARNING: No text element with name or id 'slug' was found in the 'components' layer/group. Setting slug to 'UNNAMED'.")
    else:
        Log(f"Slug found: \"{components['slug']}\"")

    if components['ModuleName'] == "Unnamed":
        Log("WARNING: No text element with name or id 'modulename' was found in the 'components' layer/group. Setting ModuleName to 'Unnamed'")
    else:
        Log(f"Module Name found: \"{components['ModuleName']}\"")

    # Scan all circles and rects for components
    components['params'] = []
    components['jacks'] = []
    components['lights'] = []
    components['alt_params'] = []

    components['legacy_knobs'] = [] #legacy only
    components['legacy_switches'] = [] #legacy only
    components['legacy_inputs'] = [] #legacy only
    components['legacy_outputs'] = [] #legacy only

    all = components_group.findall(".//svg:*",ns)

    for el in all:
        c = {}
        # Get name
        name = el.get('data-name')
        if name is None:
            name = el.get('id')
            if name is not None:
                name = remove_trailing_dash_number(name)
        if name is None:
            continue

        c['raw_name'] = name

        # If name is ElementName#ClassName, the extract ClassName
        split = name.split("#")
        if len(split) > 1:
            name = split[0]
            c['class'] = split[1]

        # If name is ElementName@pos1@pos2, then extract pos names
        c['pos_names'] = []
        c['num_choices'] = 0
        split = name.split("@")
        if len(split) == 2:
            name = split[0]
            c['num_choices'] = int(split[1])
        elif len(split) > 2:
            name = split[0]
            c['pos_names'] = split[1:]

        c['display_name'] = format_for_display(name)
        c['legacy_enum_name'] = format_as_legacy_enum_item(name)
        c['enum_name'] = format_as_enum_item(name)

        # Get position
        if el.tag == "{http://www.w3.org/2000/svg}rect":
            shape = "rect"
            x = float(el.get('x'))
            y = float(el.get('y'))
            width = float(el.get('width'))
            height = float(el.get('height'))
            c['x'] = round(x, 3)
            c['y'] = round(y, 3)
            c['width'] = round(width, 3)
            c['height'] = round(height, 3)
            c['cx'] = round(x + width / 2, 3)
            c['cy'] = round(y + height / 2, 3)
            tr = el.get('transform') 
            if tr and ("rotate(90)" in tr or "rotate(270)" in tr or "rotate(-90)" in tr):
                tmp = c['width']
                c['width'] = c['height']
                c['height'] = tmp

        elif el.tag == "{http://www.w3.org/2000/svg}circle":
            shape = "circle"
            cx = float(el.get('cx'))
            cy = float(el.get('cy'))
            c['cx'] = round(cx, 3)
            c['cy'] = round(cy, 3)
            # c['orientation'] = "Round"

        else:
            continue

        # Get color --> component type
        style = el.get('style')
        if style is None:
            print(f"Error: {shape} shape with no style found at {c['cx']}, {c['cy']}")
            continue

        color_match = re.search(r'fill:\s*(.*?);', style)
        if color_match is None:
            color_match = re.search(r'fill:\s*(.*)', style)
        color = color_match.group(1).lower() if color_match is not None else ''
        color = color.strip(";")
        color = expand_color_synonyms(color)
        c['color'] = color

        # TODO: detect Center or TopLeft coords
        c['coord_ref'] = "Center";
        default_val_int = int(color[-2:], 16)

        #Red: Knob or slider
        if color.startswith("#ff00") and default_val_int <= 128:
            c['default_val'] = str(default_val_int / 128) + "f"
            c['min_val'] = "0"
            c['max_val'] = "1"

            if shape == "circle":
                set_class_if_not_set(c, get_knob_class_from_radius(el.get('r')))
                c['category'] = "Knob"
            else:
                set_class_if_not_set(c, get_slider_class(c))
                c['category'] = "Slider"

            components['legacy_knobs'].append(c)
            components['params'].append(c)

        #Magenta: LED
        elif color.startswith("#ff00") and default_val_int > 128:
            set_class_if_not_set(c, get_led_class_from_selector(default_val_int))
            components['lights'].append(c)
            c['category'] = "Light"

        #Green: Input jack, analog (CV or audio): 
        elif color == '#00ff00':
            set_class_if_not_set(c, "AnalogJackInput4ms")
            components['legacy_inputs'].append(c)
            components['jacks'].append(c)
            c['category'] = "In"

        #Light Green: Input jack, digital (gate or trig):
        elif color == '#80ff80':
            set_class_if_not_set(c, "GateJackInput4ms")
            components['legacy_inputs'].append(c)
            components['jacks'].append(c)
            c['category'] = "In"

        #Blue: Output jack, analog (CV or audio)
        elif color == '#0000ff':
            set_class_if_not_set(c, "AnalogJackOutput4ms")
            components['legacy_outputs'].append(c)
            components['jacks'].append(c)
            c['category'] = "Out"

        #Light Blue: Output jack, digital (gate or trig):
        elif color == '#8080ff':
            set_class_if_not_set(c, "GateJackOutput4ms")
            components['legacy_outputs'].append(c)
            components['jacks'].append(c)
            c['category'] = "Out"

        #Deep Purple: Encodeer
        elif color == '#c000c0':
            set_class_if_not_set(c, get_encoder_class_from_radius(el.get('r')))
            components['legacy_knobs'].append(c)
            components['params'].append(c)
            c['category'] = "Encoder"

        #Orange: Button - Latching
        elif color == '#ff8000' or color == '#ff8001':
            set_class_if_not_set(c, "OrangeButton")
            if default_val_int == 1:
                c['default_val'] = "LatchingButton::State_t::DOWN"
            components['legacy_switches'].append(c)
            components['params'].append(c)
            c['category'] = "Button"

        #Light Orange: Button - Momentary
        elif color == '#ffc000':
            set_class_if_not_set(c, "WhiteMomentary7mm")
            components['legacy_switches'].append(c)
            components['params'].append(c)
            c['category'] = "Button"

        #Deep Pink rectangle: Switch - 2pos
        elif color == '#ff8080' or color == '#ff8081':
            set_class_if_not_set(c, get_toggle2pos_class(c))
            if default_val_int == 0x81:
                c['default_val'] = f"{c['class']}::State_t::" + ("RIGHT" if "Horiz" in c['class'] else "UP")
            components['legacy_switches'].append(c)
            components['params'].append(c)
            c['category'] = "Switch"

        #Hot Pink rectangle: Switch - 3pos
        elif color == '#ffc080' or color == '#ffc081' or color == '#ffc082':
            set_class_if_not_set(c, get_toggle3pos_class(c))
            if default_val_int == 0x81:
                c['default_val'] = f"{c['class']}::State_t::CENTER"
            elif default_val_int == 0x82:
                c['default_val'] = f"{c['class']}::State_t::" + ("RIGHT" if "Horiz" in c['class'] else "UP")
            components['legacy_switches'].append(c)
            components['params'].append(c)
            c['category'] = "Switch"

        #Yellow: Display
        elif shape == "rect" and color == '#ffff00':
            c['coord_ref'] = "TopLeft";
            set_class_if_not_set(c, "TextDisplay")
            c['category'] = "Display"
            components['lights'].append(c)

        #Medium grey: AltParam
        elif color.startswith('#8080'):
            if len(c['pos_names']) > 0:
                set_class_if_not_set(c, "AltParamChoiceLabeled")
                c['num_choices'] = len(c['pos_names'])
                c['default_val'] = str(max(0, min(c['num_choices'], default_val_int - 128)))

            elif c['num_choices'] > 0:
                set_class_if_not_set(c, "AltParamChoice")
                c['pos_names'] = []
                c['default_val'] = str(max(0, min(c['num_choices'], default_val_int - 128)))

            elif c['num_choices'] == 0:
                set_class_if_not_set(c, "AltParamContinuous")
                if default_val_int == 255:
                    default_val_int = 256
                c['default_val'] = str(default_val_int / 256) + "f"

            c['linked_region'] = []
            if shape == "rect":
                c['linked_region'] = [c['x'], c['y'], c['x'] + c['width'], c['y'] + c['height']]
           
            components['alt_params'].append(c)
            c['category'] = "AltParam"

        elif color == '#ffff00':
            Log(f"Widgets are not supported: found at {c['cx']},{c['cy']}. Skipping.")
        else:
            Log(f"Unknown color: {color} found at {c['cx']},{c['cy']}. Skipping.")

    # Find alt param links to normal params
    for alt in components['alt_params']:
        if len(alt['linked_region']) == 0:
            for p in components['params']:
                if p['cx'] == alt['cx'] and p['cy'] == alt['cy']:
                    alt['linked_param'] = p
                    break


    # Sort components
    components['legacy_knobs'].reverse()
    components['legacy_switches'].reverse()
    components['legacy_inputs'].reverse()
    components['legacy_outputs'].reverse()

    components['params'].reverse()
    components['jacks'].reverse()
    components['lights'].reverse()
    components['alt_params'].reverse()

    components['elements'] = []
    components['elements'] += components['params']
    components['elements'] += components['jacks']
    components['elements'] += components['lights']
    components['elements'] += components['alt_params']

    return components


def set_class_if_not_set(comp, newclass):
    if "class" not in comp.keys():
        comp['class'] = newclass


def components_to_infofile(components, brand="4ms"):
    slug = components['slug']
    DPI = components['dpi']

    #TODO: embed knob long name vs short name in svg
    source = "#pragma once\n"

    source += f"""#include "helpers/4ms_elements.hh"
#include "CoreModules/elements/element_info.hh"
"""

    source += f"""
#include <array>

namespace MetaModule
{{
struct {slug}Info : ModuleInfoBase {{
    static constexpr std::string_view slug{{"{slug}"}};
    static constexpr std::string_view description{{"{components['ModuleName']}"}};
    static constexpr uint32_t width_hp = {components['HP']};
    static constexpr std::string_view svg_filename{{"res/modules/{slug}.svg"}};
    static constexpr std::string_view png_filename{{"{brand}/{slug}.png"}};

    using enum Coords;

    static constexpr std::array<Element, {len(components['elements'])}> Elements{{{{
{list_elem_definitions(components['elements'], DPI)}}}}};

    enum class Elem {{{list_elem_names(components['elements'])}
    }};

    // Legacy naming (safe to remove once all legacy 4ms CoreModules are converted)
    {make_legacy_enum("Knob", components['legacy_knobs'])}
    {make_legacy_enum("Switch", components['legacy_switches'])}
    {make_legacy_enum("Input", components['legacy_inputs'])}
    {make_legacy_enum("Output", components['legacy_outputs'])}
    {make_legacy_enum("Led", components['lights'])}
    {make_legacy_enum("AltParam", components['alt_params'])}
}};
}} // namespace MetaModule
"""
    return source


def list_elem_definitions(elems, DPI):
    # TODO: use AltParam linked_region and linked_param

    if len(elems) == 0:
        return ""
    source = ""
    for k in elems:
        source += "\t\t"
        source += f"{k['class']}{{{{"
        if k['class'] == "AltParamChoiceLabeled":
            source += f"{{"
        if k['coord_ref'] == "Center":
            source += f"to_mm<{DPI}>({k['cx']}), "
            source += f"to_mm<{DPI}>({k['cy']}), "
        else:
            source += f"to_mm<{DPI}>({k['x']}), "
            source += f"to_mm<{DPI}>({k['y']}), "
        source += f"{k['coord_ref']}, "
        source += f"\"{k['display_name']}\", "
        source += f"\"\"" #long name
        source += print_size(k, DPI)
        source += f"}}"
        source += print_position_names(k)
        source += print_default_value(k)
        source += f"""}},
"""
    return source

def print_position_names(elem):
    TwoPosSwitches = ["Toggle2pos", "Toggle2posHoriz"]
    ThreePosSwitches = ["Toggle3pos", "Toggle3posHoriz"]

    if "pos_names" not in elem.keys() and "num_choices" not in elem.keys():
        return ""

    elif elem['class'] in ThreePosSwitches and len(elem['pos_names']) == 3:
        return f""", {{"{elem['pos_names'][0]}", "{elem['pos_names'][1]}", "{elem['pos_names'][2]}"}}""" 

    elif elem['class'] in TwoPosSwitches and len(elem['pos_names']) == 2:
        return f""", {{"{elem['pos_names'][0]}", "{elem['pos_names'][1]}"}}""" 

    elif elem['class'] == "AltParamChoice":
        return f""", {elem['num_choices']}""" 

    elif elem['class'] == "AltParamChoiceLabeled":
        if "default_val" in elem:
            defaultval = f", {elem['default_val']}"
            del elem['default_val'] #prevent it from being added again
        else:
            defaultval = ""
        source = f""", {elem['num_choices']}{defaultval}}}, {{"""
        for nm in elem['pos_names']:
            source += f""""{nm}", """
        source = source.removesuffix(", ")
        source += f"""}}"""

        return source

    else:
        return ""


def print_default_value(elem):
    if "default_val" in elem:
        return f""", {elem["default_val"]}""" 
    else:
        return ""

def print_size(elem, DPI):
    if elem['category'] == "Display":
        return f", to_mm<{DPI}>({elem['width']}), to_mm<{DPI}>({elem['height']})"
    else:
        return ""

def list_elem_names(elems):
    if len(elems) == 0:
        return ""
    source = ""
    for k in elems:
        name = k['enum_name']
        if not k['enum_name'].endswith(k['category']):
            name = k['enum_name']+k['category']
        source += f"""
        {name},"""
    return source


def make_legacy_enum(item_prefix, elements):
    if len(elements) == 0:
        return ""
    source = f"""
    enum {{"""
    i = 0
    for k in elements:
        source += f"""
        {item_prefix}{k['legacy_enum_name']}, """
        i = i + 1
    if item_prefix == "Knob":
           source += """
        NumKnobs,"""
    elif item_prefix == "Switch":
           source += """
        NumSwitches,"""
    elif item_prefix == "Input":
           source += """
        NumInJacks,"""
    elif item_prefix == "Output":
           source += """
        NumOutJacks,"""
    elif item_prefix == "Led":
           source += """
        NumDiscreteLeds,"""

    source += f"""
    }};"""
    return source

