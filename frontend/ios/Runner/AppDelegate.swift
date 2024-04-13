import UIKit
import Flutter
import Firebase

@UIApplicationMain
@objc class AppDelegate: FlutterAppDelegate {
  override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    // Configure Firebase before registering plugins
    FirebaseApp.configure()
    
    do {
      // Register plugins after Firebase configuration to avoid any potential conflicts
      try GeneratedPluginRegistrant.register(with: self)
    } catch {
      // Handle any errors that occur during plugin registration
      print("Error registering plugins: \(error)")
      return false
    }
    
    // Call super.application(application, didFinishLaunchingWithOptions: launchOptions) last
    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }
}
