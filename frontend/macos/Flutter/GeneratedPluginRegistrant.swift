// Registers generated Flutter plugins with the given FlutterPluginRegistry.
func RegisterGeneratedPlugins(registry: FlutterPluginRegistry) {
    
    // Register Firebase Analytics plugin
    FLTFirebaseAnalyticsPlugin.register(with: registry.registrar(forPlugin: "FLTFirebaseAnalyticsPlugin"))
    
    // Register Firebase Auth plugin
    FLTFirebaseAuthPlugin.register(with: registry.registrar(forPlugin: "FLTFirebaseAuthPlugin"))
    
    // Register Firebase Core plugin
    FLTFirebaseCorePlugin.register(with: registry.registrar(forPlugin: "FLTFirebaseCorePlugin"))
    
    // Register Shared Preferences plugin
    SharedPreferencesPlugin.register(with: registry.registrar(forPlugin: "SharedPreferencesPlugin"))
    
    // Register Url Launcher plugin
    UrlLauncherPlugin.register(with: registry.registrar(forPlugin: "UrlLauncherPlugin"))
}
