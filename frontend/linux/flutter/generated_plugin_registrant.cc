//
//  Generated file. Do not edit.
//

// clang-format off

#include "generated_plugin_registrant.h"
#include <url_launcher_linux/url_launcher_plugin.h>

/*
 * Register plugins with the FlPluginRegistry.
 */
void register_plugins(FlPluginRegistry* registry) {
  g_autoptr(FlPluginRegistrar) url_launcher_linux_registrar =
      fl_plugin_registry_get_registrar_for_plugin(registry, "UrlLauncherPlugin");
  
  // Register url_launcher_linux plugin
  url_launcher_plugin_register_with_registrar(url_launcher_linux_registrar);
}

