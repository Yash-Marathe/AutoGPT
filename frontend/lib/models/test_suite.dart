import 'package:auto_gpt_flutter_client/models/task.dart';

class TestSuite {
  final String timestamp;
  final List<Task> tests;

  TestSuite({required this.timestamp, required this.tests});

  // Serialization: Convert the object into a Map
  Map<String, dynamic> toJson() {
    return {
      'timestamp': timestamp,
      'tests': tests.map((task) => task.toJson()).toList(),
    };
  }

  // Deserialization: Create an object from a Map
  factory TestSuite.fromJson(Map<String, dynamic> json) {
    return TestSuite(
      timestamp: json['timestamp'],
      tests: (json['tests'] as List)
          .map((taskJson) => Task.fromJson(taskJson))
          .toList(),
    );
  }

  // Factory constructor for a TestSuite with empty tests list
  factory TestSuite.empty() {
    return TestSuite(timestamp: '', tests: const []);
  }

  // Static method to create a TestSuite from a JSON string
  static TestSuite fromJsonString(String jsonString) {
    final json = jsonDecode(jsonString);
    return TestSuite.fromJson(json);
  }
}
