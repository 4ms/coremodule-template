# CoreModule Template

This is a template project for creating a plugin of CoreModules, and 
compiling it as a MetaModule plugin and a VCV Rack plugin.

## Prerequisites
To build, make sure you set RACK_DIR to point to the Rack SDK on your computer.
You will also need all the prerequisites required to build Rack. Read how here:
https://vcvrack.com/manual/PluginDevelopmentTutorial#Prerequisites

The MetaModule SDK is already a submodule of this repo, but you can use a
different MetaModule SDK if you wish (see below).

You also need the following in order to build the MetaModule plugin:
- cmake v3.24 or later
- ninja (not required if you configure cmake to use a different generator)
- arm-none-eabi-gcc toolchain 12.2 or 12.3, installed on your PATH
- python 3.6 or later


Make sure to clone the submodules recursively:

```
git clone https://github.com/4ms/coremodule-template.git
cd coremodule-template
git submodule update --init --recursive
```

## Building

To build just the MetaModule plugin:
```
make mm
```

To build just the Rack plugin:
```
make all
```

To build both plugins:
```
make all mm
```

To package and install the Rack plugin:
```
make install
```

To install the MetaModule plugin, copy the file in `metamodule-plugins/` that
ends in `.mmplugin` to the `metamodule-plugins/` folder on an SD Card or USB
drive. You can do this in your OS, or use the command-line:

```
cp metamodule-plugins/*.mmplugin /Volumes/MyUsbDrive/metamodule-plugins/    # For example
```

To clean the build for both plugins:
```
make clean
```

To re-configure the MetaModule plugin cmake build:
```
make config
```


## Using a different MetaModule SDK

To use a different version of the SDK, you have some options.

One way is to checkout a different branch in the SDK submodule:

```
cd metamodule-plugin-sdk
git checkout v2.0-dev                 # For example, to checkout the v2.0-dev branch
git submodule update --recursive
cd ..
```

Another option is to use a cmake variable to point to the SDK you want to use on your computer:

```
make config METAMODULE_SDK_DIR=/full/path/to/metamodule-plugin-sdk
```

You can also specify where the .mmplugin file goes like this:

```
make config METAMODULE_SDK_DIR=/path/SDK-v2/metamodule-plugin-sdk INSTALL_DIR=metamodule-plugins-v2
make mm

make config METAMODULE_SDK_DIR=/path/SDK-v1/metamodule-plugin-sdk INSTALL_DIR=metamodule-plugins-v1
make mm
```

Note that the INSTALL_DIR is relative to the build/ dir, so if you did the
above commands, you'd see the plugins in build/:

```
ls -l build

    ...
    drwxr-xr-x   3 user  group       96 Mar 20 11:49 metamodule-plugins-v1/
    drwxr-xr-x   3 user  group       96 Mar 20 11:49 metamodule-plugins-v2/
    ...

ls -l build/metamodule-plugins-v1/

    -rw-r--r--  1 user  group  26624 Mar 20 11:49 MyPlugin.mmplugin

ls -l build/metamodule-plugins-v2/

    -rw-r--r--  1 user  group  26600 Mar 20 11:49 MyPlugin.mmplugin
```

## Creating an info file

The `info` file is a header file that contains a description of all the elements in a module (jacks, knobs, switches, etc).
It also provides the module slug, faceplate location, and bypass routes.

By convention, info headers are named `Slug_info.hh` where Slug is the module slug.

In this repo, the info file(s) are in `src/modules/info/`

While you can write this by hand, getting the XY positions to match the artwork file is tedious. So, there's a script that
does this automatically.

First, create an SVG file for your modules.

Create two layers (Illustrator) or "groups" (Inkscape). One is named "components" and the other is named "faceplate".

Draw all artwork in the "faceplate" layer. If you use fonts, convert them to outlines.

In the components layer, make various shapes to indicate the location and type of each kind of element.

Read the file `SPECS.md` found in `scripts/svgextract` for instructions on how to to do that.

Very important is to read the part about the slug and modulename text objects.
You must have two text objects (not converted to outlines) on the components
layer (don't worry, they won't show up on your artwork!). The slug object is the module slug,
and the modulename object is a longer description.

When you have the SVG file, run the svgextract python script on it to create an info file:

```
python3 scripts/svgextract/svgextract.py createinfo src/modules/svg/MyModule_info.svg src/modules/info/

```

This will create a file named `MyModule_info.hh` in src/modules/info


Open this file and edit the paths to the faceplate files (svg_filename and png_filename).
The script can't know how you organize these files, so you have to do this manually.

svg_filename is the VCV rack panel artwork. This will be something like `res/panel.svg`. 

png_filename is the MetaModule artwork. This must start with your brand slug, that is, the plugin name (`MyPlugin/panel.svg`).
