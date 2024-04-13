//
//  Generated file. Do not edit.
//

// Includes for the plugins to be registered.
#include <firebase_core/firebase_core_plugin_c_api.h>
#include <url_launcher_windows/url_launcher_windows.h>

// Include the Flutter plugin registry.
#include "flutter/flutter_plugin_registry.h"

// Registers the specified plugins with the given plugin registry.
void RegisterPlugins(flutter::PluginRegistry* registry) {
  // Registers the Firebase Core plugin.
  FirebaseCorePluginCApiRegisterWithRegistrar(
      registry->GetRegistrarForPlugin("FirebaseCorePluginCApi"));

  // Registers the Url Launcher plugin for Windows.
  UrlLauncherWindowsRegisterWithRegistrar(
      registry->GetRegistrarForPlugin("UrlLauncherWindows"));
}
