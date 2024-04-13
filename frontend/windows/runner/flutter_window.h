#ifndef RUNNER_FLUTTER_WINDOW_H_
#define RUNNER_FLUTTER_WINDOW_H_

#include <flutter/dart_project.h>
#include <flutter/flutter_view_controller.h>

#include <memory>
#include <string>

#include "win32_window.h"

// A window that hosts a Flutter view.
class FlutterWindow : public Win32Window {
 public:
  // Creates a new FlutterWindow hosting a Flutter view running the project at
  // the given |project_path|.
  explicit FlutterWindow(const std::string& project_path);
  virtual ~FlutterWindow();

  // Creates and shows the FlutterWindow.
  static FlutterWindow* CreateAndShow();

 protected:
  // Win32Window:
  bool OnCreate() override;
  void OnDestroy() override;
  LRESULT MessageHandler(HWND window, UINT const message, WPARAM const wparam,
                         LPARAM const lparam) noexcept override;

 private:
  // Creates and initializes the FlutterViewController.
  bool CreateFlutterController();

  // Handles the WM_SIZE message.
  void OnSize(UINT const message, WPARAM const wparam, LPARAM const lparam);

  // Handles the WM_PAINT message.
  void OnPaint();

  // The path to the project to run.
  std::string project
