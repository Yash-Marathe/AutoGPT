#include <flutter/dart_project.h>
#include <flutter/flutter_view_controller.h>
#include <flutter/flutter_window.h>
#include <flutter/shell/platform_view_delegate_windows.h>
#include <windows.h>

#include "utils.h"

int APIENTRY wWinMain(_In_ HINSTANCE instance, _In_opt_ HINSTANCE prev,
                      _In_ wchar_t *command_line, _In_ int show_command) {
  // Attach to console when present (e.g., 'flutter run') or create a
  // new console when running with a debugger.
  if (!::AttachConsole(ATTACH_PARENT_PROCESS) && ::IsDebuggerPresent()) {
    CreateAndAttachConsole();
  }

  // Initialize COM, so that it is available for use in the library and/or
  // plugins.
  ::CoInitializeEx(nullptr, COINIT_APARTMENTTHREADED);

  flutter::DartProject project(L"data");

  std::vector<std::string> command_line_arguments =
      GetCommandLineArguments();

  project.set_dart_entrypoint_arguments(std::move(command_line_arguments));

  auto window_delegate = std::make_unique<flutter::PlatformViewDelegateWindows>();
  auto view = flutter::FlutterViewController::Create(
      std::move(project), std::move(window_delegate));

  Win32Window::Point origin(10, 10);
  Win32Window::Size size(1280, 720);
  HWND hwnd = view->CreateWindow(nullptr, L"auto_gpt_flutter_client", origin, size);
  if (!hwnd) {
    // Log the error
    DWORD errCode = GetLastError();
    LPVOID lpMsgBuf;
    FormatMessage(
        FORMAT_MESSAGE_ALLOCATE_BUFFER | FOR
