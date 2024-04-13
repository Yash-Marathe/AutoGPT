#include "utils.h"

#include <flutter_windows.h>
#include <io.h>
#include <stdio.h>
#include <windows.h>

#include <iostream>
#include <vector>

bool CreateConsoleIfNecessary() {
  if (_isatty(_fileno(stdout)) && _isatty(_fileno(stderr))) {
    // The process already has a console window.
    return false;
  }

  if (!::AllocConsole()) {
    // Failed to create a console window.
    std::cerr << "Failed to create a console window: " << ::GetLastError() << std::endl;
    return false;
  }

  FILE* unused;
  if (!freopen_s(&unused, "CONOUT$", "w", stdout)) {
    _dup2(_fileno(stdout), 1);
  } else {
    std::cerr << "Failed to redirect stdout to the console window: " << ::GetLastError() << std::endl;
    ::FreeConsole();
    return false;
  }

  if (!freopen_s(&unused, "CONOUT$", "w", stderr)) {
    _dup2(_fileno(stdout), 2);
  } else {
    std::cerr << "Failed to redirect stderr to the console window: " << ::GetLastError() << std::endl;
    ::FreeConsole();
    return false;
  }

  std::ios::sync_with_stdio();
  FlutterDesktopResyncOutputStreams();

  return true;
}

std::vector<std::string> ConvertCommandLineArguments(int argc, wchar_t** argv) {
  std::vector<std::string> command_line_arguments;

  // Skip the first argument as it's the binary name.
  for (int i = 1; i < argc; i++) {
    command_line_arguments.push_back(Utf8FromUtf16(argv[i]));
  }

  return command_line_arguments;
}

std::string Utf8FromUtf16(const wchar_t* utf16_string) {
  if (utf16_string == nullptr) {
    return std::string();
  }


