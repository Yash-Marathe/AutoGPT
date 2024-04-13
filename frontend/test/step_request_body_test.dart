import 'package:auto_gpt_flutter_client/models/step_request_body.dart';
import 'package:flutter_test/flutter_test.dart';
import 'dart:convert';

void main() {
  group('StepRequestBody', () {
    test('creates StepRequestBody with correct values', () {
      final stepRequestBody = StepRequestBody(
        input: 'Execute something',
        additionalInput: {'key': 'value'},
      );

      expect(stepRequestBody.input, 'Execute something');
      expect(stepRequestBody.additionalInput, {'key': 'value'});
    });

    test('converts StepRequestBody to correct JSON', () {
      final stepRequestBody = StepRequestBody(
        input: 'Execute something',
        additionalInput: {'key': 'value'},
      );

      final json = jsonEncode(stepRequestBody.toJson());

      expect(json, '{"input":"Execute something","additional_input":{"key":"value"}}');
    });

    test('parses JSON to StepRequestBody', () {
      const jsonString = '{"input":"Execute something","additional_input":{"key":"value"}}';
      final json = jsonDecode(jsonString);

      final stepRequestBody = StepRequestBody.fromJson(json);

      expect(stepRequestBody.input, 'Execute something');
      expect(stepRequestBody.additionalInput, {'key': 'value'});
    });
  });
}
