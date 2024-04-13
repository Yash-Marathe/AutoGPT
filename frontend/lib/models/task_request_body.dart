import 'dart:convert';

class TaskRequestBody {
  final String input;
  final Map<String, dynamic>? additionalInput;

  TaskRequestBody({required this.input, this.additionalInput});

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> jsonMap = {'input': input};
    if (additionalInput != null) {
      jsonMap['additional_input'] = additionalInput;
    }
    return jsonMap;
  }

  /// Returns a TaskRequestBody object constructed from a JSON object
  factory TaskRequestBody.fromJson(Map<String, dynamic> json) {
    return TaskRequestBody(
      input: json['input'],
      additionalInput: json['additional_input'],
    );
  }

  /// Returns a JSON string representation of this object
  String toJsonString() {
    final jsonBody = jsonEncode(toJson());
    return jsonBody;
  }

  /// Creates a TaskRequestBody object from a JSON string
  factory TaskRequestBody.fromJsonString(String jsonString) {
    final jsonBody = jsonDecode(jsonString);
    return TaskRequestBody.fromJson(jsonBody);
  }
}
