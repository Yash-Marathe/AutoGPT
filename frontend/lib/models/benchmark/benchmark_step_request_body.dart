import 'dart:convert';

class BenchmarkStepRequestBody {
  final String? input;

  BenchmarkStepRequestBody({required this.input});

  Map<String, dynamic> toJson() {
    Map<String, dynamic> jsonMap = {};
    if (input != null) {
      jsonMap['input'] = input;
    }
    return jsonMap;
  }

  /// Returns a JSON-encoded string version of this object.
  String toJsonString() => json.encode(toJson());

  /// Creates a BenchmarkStepRequestBody object from a JSON-encoded string.
  factory BenchmarkStepRequestBody.fromJsonString(String jsonString) {
    final jsonMap = json.decode(jsonString);
    return BenchmarkStepRequestBody(
      input: jsonMap['input'] as String?,
    );
  }
}
