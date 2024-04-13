#include "flutter_window.h"

#include <optional>

#include "flutter/generated_plugin_registrant.h"

/**
 * Constructor for FlutterWindow class.
 * @param project The Flutter project to use for the window.
 */
FlutterWindow::FlutterWindow(const flutter::DartProject& project)
    : project_(project) {}

/**
 * Destructor for FlutterWindow class.
 */
FlutterWindow::~FlutterWindow() {}

/**
 * Handles the creation of the window.
 * @return True if the window was created successfully, false otherwise.
 */
bool FlutterWindow::OnCreate() {
  if (!Win32Window::OnCreate()) {
    return false;
  }

  RECT frame = GetClientArea();

  // The size here must match the window dimensions to avoid unnecessary surface
  // creation / destruction in the startup path.
  flutter_controller_ = std::make_unique<flutter::FlutterViewController>(
      frame.right - frame.left, frame.bottom - frame.top, project_);

  // Ensure that basic setup of the controller was successful.
  if (!flutter_controller_->engine() || !flutter_controller_->view()) {
    return false;
  }

  RegisterPlugins(flutter_controller_->engine());
  SetChildContent(flutter_controller_->view()->GetNativeWindow());

  flutter_controller_->engine()->SetNextFrameCallback([&]() {
    this->Show();
  });

  return true;
}

/**
 * Handles the destruction of the window.
 */
void FlutterWindow::OnDestroy() {
  if (flutter_controller_) {
    flutter_controller_ = nullptr;
  }

  Win32Window::OnDestroy();
}

/**
 * Handles messages for the window.
 * @param hwnd The handle to the window.
 * @param message The message to handle.
 * @param wparam The wparam value for the message.
 * @param lparam The lparam value for the message.
 * @return The result of handling the message.
 */
LRESULT
FlutterWindow::MessageHandler(HWND hwnd, UINT const message,
                              WPARAM const wparam,
                              LPARAM const lparam) noexcept {
  // Give Flutter, including plugins, an opportunity to handle window messages.
  if (flutter_controller_) {
    std::optional<LRESULT> result =
        flutter_controller_->HandleTopLevelWindowProc(hwnd, message, wparam,
                                                      lparam);
    if (result) {
      return *result;
    }
  }

  switch (message) {
    case WM_FONTCHANGE:
      flutter_controller_->
