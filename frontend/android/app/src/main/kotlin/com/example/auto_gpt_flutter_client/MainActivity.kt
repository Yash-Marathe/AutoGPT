// Import the necessary packages and classes
package com.example.auto_gpt_flutter_client

import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugins.GeneratedPluginRegistrant

// Define the main activity class that inherits from FlutterActivity
class MainActivity: FlutterActivity() {
    // Override the configureFlutterEngine method to register plugins
    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        // Generate the plugin registrant and register all the plugins
        GeneratedPluginRegistrant.registerWith(flutterEngine);
    }
}
