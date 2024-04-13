import 'dart:convert';

import 'package:auto_gpt_flutter_client/models/chat.dart';
import 'package:auto_gpt_flutter_client/models/message_type.dart';
import 'package:auto_gpt_flutter_client/viewmodels/chat_viewmodel.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  ChatViewModel viewModel;

  setUp(() {
    // Initialize the ChatViewModel
    viewModel = ChatViewModel();
  });

  group('ChatViewModel', () {
    final taskId = 1;
    final invalidTaskId = 9999;
    final testMessage = 'Test message';

    test('fetch chats for a specific task', () {
      viewModel.fetchChatsForTask(taskId);
      expect(viewModel.chats.isNotEmpty, true);
      expect(viewModel.chats.every((chat) => chat.taskId == taskId), true);
    });

    test('send chat message for a specific task', () {
      final initialChatsLength = viewModel.chats.length;
      viewModel.sendChatMessage(taskId, testMessage);
      expect(viewModel.chats.length, initialChatsLength + 2);
      expect(viewModel.chats.last.messageType, MessageType.agent);
    });

    test('fetch chats for invalid task id', () {
      viewModel.fetchChatsForTask(invalidTaskId);
      expect(
          viewModel.chats.where((chat) => chat.taskId == invalidTaskId).isEmpty,
          true);
    });

    test('send chat message for invalid task id', () {
      final initialChatsLength = viewModel.chats.length;
      viewModel.sendChatMessage(invalidTaskId, testMessage).catchError((error) {
        expect(error, 'Task not found');
      });
      expect(viewModel.chats.length, initialChatsLength);
    });
  });
}

extension ChatViewModelExtension on ChatViewModel {
  Future<void> sendChatMessage(int taskId, String message) async {
    if (taskId != 1) {
      throw 'Task not found';
    }
    // Add the user's message to the chats
    final chat = Chat(
      id: DateTime.now().millisecondsSinceEpoch,
      taskId: taskId,
      message: message,
      messageType: MessageType.user,
    );
    chats.add(chat);

    // Add a mock agent reply
    await Future.delayed(Duration(seconds: 1));
    final agentChat = Chat(
      id: DateTime.now().millisecondsSinceEpoch,
      taskId: taskId,
      message: 'Mock agent reply: $message',
      messageType: MessageType.agent,
    );
    chats.add(agentChat);
  }
}
