import FlutterMacOS
import Cocoa
import XCTest

class RunnerTests: XCTestCase {

    func testFlutterVersion() {
        let app = FlutterMacOSApplication(url: Bundle.main.bundleURL) as! NSApplication
        let flutterView = FlutterView(frame: .zero)
        app.delegate = FlutterMacOSApplicationDelegate(machPort: RunLoop.current.machPort, view: flutterView)
        XCTAssertNotNil(flutterView.engine, "Flutter engine is not initialized")
        XCTAssertTrue(flutterView.engine!.runner!.flutterVersion.hasSuffix("."), "Invalid Flutter version format")
    }

}
