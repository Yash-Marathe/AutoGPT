# This file controls Flutter-level build steps. It should not be edited.

# Project name
project(FlutterBuild)

# Minimum required version of CMake
cmake_minimum_required(VERSION 3.14)

# Enable/Disable the generation of the ephemeral directory
option(GENERATE_EPHEMERAL "Generate ephemeral directory" ON)

if(GENERATE_EPHEMERAL)
  # Add the subdirectory that generates the ephemeral directory
  add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/ephemeral)
endif()

# Configuration provided via flutter tool.
include(${EPHEMERAL_DIR}/generated_config.cmake)

# === Flutter Library ===
set(FLUTTER_LIBRARY "${EPHEMERAL_DIR}/flutter_windows.dll")

# Published to parent scope for install step.
set(FLUTTER_LIBRARY ${FLUTTER_LIBRARY} PARENT_SCOPE)
set(FLUTTER_ICU_DATA_FILE "${EPHEMERAL_DIR}/icudtl.dat" PARENT_SCOPE)
set(PROJECT_BUILD_DIR "${PROJECT_DIR}/build/" PARENT_SCOPE)
set(AOT_LIBRARY "${PROJECT_DIR}/build/windows/app.so" PARENT_SCOPE)

# Include directories for the flutter library
target_include_directories(flutter INTERFACE
  "${EPHEMERAL_DIR}"
)

# Link libraries for the flutter library
target_link_libraries(flutter INTERFACE "${FLUTTER_LIBRARY}.lib")

# === Wrapper ===
# Sources for the wrapper
set(CPP_WRAPPER_SOURCES_CORE
  "core_implementations.cc"
  "standard_codec.cc"
)
set(CPP_WRAPPER_SOURCES_PLUGIN
  "plugin_registrar.cc"
)
set(CPP_WRAPPER_SOURCES_APP
  "flutter_engine.cc"
  "flutter_view_controller.cc"
)

# Wrapper library for plugins
add_library(flutter_wrapper_plugin STATIC
  ${CPP_WRAPPER_SOURCES_CORE}
  ${CPP_WRAPPER_SOURCES_PLUGIN}
)

# Set properties for the flutter_wrapper_plugin library
set_target_properties(flutter_wrapper_plugin PROPERTIES
  POSITION_INDEPENDENT_CODE ON)
set_target_properties(flutter_wrapper_plugin PROPERTIES
  CXX_VISIBILITY_PRESET hidden)

# Include directories for the flutter_wrapper_plugin library
target_include_directories(flutter_wrapper_plugin PUBLIC
  "${WRAPPER_ROOT}/include"
)

# Link libraries for the flutter_wrapper_plugin library
target_link_libraries(flutter_wrapper_plugin PUBLIC flutter)

# Wrapper library for the runner
add_library(flutter_wrapper_app STATIC
  ${CPP_WRAPPER_SOURCES_CORE}
  ${CPP_WRAPPER_SOURCES_APP}
)

# Set properties for the flutter_wrapper_app library
set_target_properties(flutter_wrapper_app PROPERTIES
  POSITION_INDEPENDENT_CODE ON)
set_target_properties(flutter_wrapper_app PROPERTIES
  CXX_VISIBILITY_PRESET hidden)

# Include directories for the flutter_wrapper_app library
target_include_directories(flutter_wrapper_app PUBLIC
  "${WRAPPER_ROOT}/include"
)

# Link libraries for the flutter_wrapper_app library
target_link_libraries(flutter_wrapper_app PUBLIC flutter)

# === Flutter tool backend ===
# Phony output file
set(PHONY_OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/_phony_")
set_source_files_properties("${PHONY_OUTPUT}" PROPERTIES SYMBOLIC TRUE)

# Custom command to generate the required files
add_custom_command(
  OUTPUT ${FLUTTER_LIBRARY} ${FLUTTER_LIBRARY_HEADERS}
    ${CPP_WRAPPER_SOURCES_CORE} ${CPP_WRAPPER_SOURCES_PLUGIN}
    ${CPP_WRAPPER_SOURCES_APP}
    ${PHONY_OUTPUT}
  COMMAND ${CMAKE_COMMAND} -E env
    ${FLUTTER_TOOL_ENVIRONMENT}
    "${FLUTTER_ROOT}/packages/flutter_tools/bin/tool_backend.bat"
      windows-x64 $<CONFIG>
  VERBATIM
)

# Custom target to depend on the generated files
add_custom_target(flutter_assemble DEPENDS
  "${FLUTTER_LIBRARY}"
  ${FLUTTER_LIBRARY_HEADERS}
  ${CPP_WRAPPER_SOURCES_CORE}
  ${CPP_WRAPPER_SOURCES_PLUGIN}
  ${CPP_WRAPPER_SOURCES_APP}
)

# Install the required files
