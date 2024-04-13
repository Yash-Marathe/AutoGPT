import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:auto_gpt_flutter_client/models/task_request_body.dart';

void main() {
  group('TaskRequestBody', () {
    test('creates TaskRequestBody with correct values', () {
      final taskRequestBody = TaskRequestBody(
        input: 'Do something',
        additionalInput: {'key': 'value'},
      );

      expect(taskRequestBody.input, 'Do something');
      expect(taskRequestBody.additionalInput, {'key': 'value'});
    });

    test('converts TaskRequestBody to correct JSON', () {
      final taskRequestBody = TaskRequestBody(
        input: 'Do something',
        additionalInput: {'key': 'value'},
      );

      final json = jsonEncode(taskRequestBody);

      final expectedJson = '''
      {
        "input": "Do something",
        "additional_input": {
          "key": "value"
        }
      }
      ''';

      expect(json, expectedJson);
    });

    test('parses JSON to TaskRequestBody', () {
      final json = '''
      {
        "input": "Do something",
        "additional_input": {
          "key": "value"
        }
      }
      ''';

      final taskRequestBody = TaskRequestBody.fromJson(jsonDecode(json));

      expect(taskRequestBody.input, 'Do something');
      expect(taskRequestBody.additionalInput, {'key': 'value'});
    });
  });
}
