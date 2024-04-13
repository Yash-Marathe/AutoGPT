#ifndef RUNNER_UTILS_H_
#define RUNNER_UTILS_H_

#include <string>
#include <vector>
#include <codecvt>
#include <locale>

// Creates a console for the process, and redirects stdout and stderr to
// it for both the runner and the Flutter library.
inline void CreateAndAttachConsole() {}

// Takes a null-terminated wchar_t* encoded in UTF-16 and returns a std::string
// encoded in UTF-8. Returns an empty std::string on failure.
inline std::string Utf8FromUtf16(const wchar_t* utf16_string) {
  std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;
  return converter.to_bytes(utf16_string);
}

// Gets the command line arguments passed in as a std::vector<std::string>,
// encoded in UTF-8. Returns an empty std::vector<std::string> on failure.
inline std::vector<std::string> GetCommandLineArguments() {
  std::vector<std::string> args;
  for (auto arg : std::vector<wchar_t*>(__wargv, __wargv + __wargc)) {
    args.push_back(Utf8FromUtf16(arg));
  }
  return args;
}

#endif  // RUNNER_UTILS_H_
