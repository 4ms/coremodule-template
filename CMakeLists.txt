cmake_minimum_required(VERSION 3.22)

if(NOT "${METAMODULE_SDK_DIR}" STREQUAL "")
	message("METAMODULE_SDK_DIR set by CMake variable ${METAMODULE_SDK_DIR}")
elseif (DEFINED ENV{METAMODULE_SDK_DIR})
    set(METAMODULE_SDK_DIR "$ENV{METAMODULE_SDK_DIR}")
	message("METAMODULE_SDK_DIR set by environment variable ${METAMODULE_SDK_DIR}")
else()
    set(METAMODULE_SDK_DIR "${CMAKE_CURRENT_LIST_DIR}/../metamodule-plugin-sdk")
	message("METAMODULE_SDK_DIR set to default: ${METAMODULE_SDK_DIR}")
endif()

include(${METAMODULE_SDK_DIR}/plugin.cmake)

project(CoreModule_MetaModulePlugin 
    VERSION     0.1
    DESCRIPTION "CoreModule Template Plugin for MetaModule"
    LANGUAGES   C CXX ASM
)

add_library(MyPlugin STATIC)


file(GLOB sources src/modules/core/*.cc)

target_sources(MyPlugin
    PRIVATE
    ${sources}
    src/mm-plugin.cc
)

target_include_directories(MyPlugin PRIVATE
    src/
    src/helpers/
)

target_compile_options(MyPlugin
    PRIVATE

)
