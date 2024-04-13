import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:auto_gpt_flutter_client/views/chat/chat_input_field.dart';

void main() {
  group('ChatInputField tests:', () {
    Widget _buildChatInputField({required VoidCallback onSendPressed}) {
      return MaterialApp(
        home: Scaffold(
          body: ChatInputField(
            onSendPressed: onSendPressed,
          ),
        ),
      );
    }

    testWidgets('renders correctly', (WidgetTester tester) async {
      await tester.pumpWidget(_buildChatInputField(onSendPressed: () {}));

      expect(find.byType(TextField), findsOneWidget);
      expect(find.byIcon(Icons.send), findsOneWidget);
    });

    testWidgets('text field accepts input', (WidgetTester tester) async {
      bool inputChanged = false;

      await tester.pumpWidget(_buildChatInputField(onSendPressed: () {}));

      await tester.enterText(find.byType(TextField), 'Hello');
      await tester.pump();

      expect(find.text('Hello'), findsOneWidget);
      expect(inputChanged, isTrue);
    });

    testWidgets('send button triggers callback', (WidgetTester tester) async {
      bool callbackCalled = false;

      await tester.pumpWidget(_buildChatInputField(onSendPressed: () {
        callbackCalled = true;
      }));

      await tester.tap(find.byIcon(Icons.send));
      await tester.pump();

      expect(callbackCalled, isTrue);
    });
  });
}
