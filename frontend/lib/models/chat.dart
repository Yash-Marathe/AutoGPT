import 'package:auto_gpt_flutter_client/models/artifact.dart';
import 'package:auto_gpt_flutter_client/models/message_type.dart';
import 'package:json_pointer/json_pointer.dart';

/// Represents a chat message related to a specific task.
class Chat {
  final String id;
  final String taskId;
  final String message;
  final DateTime timestamp;
  final MessageType messageType;
  final Map<String, dynamic>? jsonResponse;
  final List<Artifact> artifacts;

  Chat({
    required this.id,
    required this.taskId,
    required this.message,
    required this.timestamp,
    required this.messageType,
    this.jsonResponse,
    required this.artifacts,
  });

  // Convert a Map (usually from JSON) to a Chat object
  factory Chat.fromMap(Map<String, dynamic> map) {
    return Chat(
      id: map['id'] as String,
      taskId: map['taskId'] as String,
      message: map['message'] as String,
      timestamp: DateTime.parse(map['timestamp'] as String),
      messageType: MessageType.values.firstWhere(
          (e) => e.toString() == 'MessageType.${map['messageType']}'),
      jsonResponse: map['jsonResponse'] as Map<String, dynamic>?,
      artifacts: (map['artifacts'] as List<dynamic>)
          .map((artifact) => Artifact.fromJson(artifact as Map<String, dynamic>))
          .toList(),
    );
  }

  Map<String, dynamic> toJson() {
    final json = <String, dynamic>{
      'id': id,
      'taskId': taskId,
      'message': message,
      'timestamp': timestamp.toIso8601String(),
      'messageType': messageType.toString(),
      'jsonResponse': jsonResponse,
      'artifacts': artifacts.map((artifact) => artifact.toJson()).toList(),
    };

    return json;
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is Chat &&
          runtimeType == other.runtimeType &&
          id == other.id &&
          taskId == other.taskId &&
          message == other.message &&
          timestamp == other.timestamp &&
          messageType == other.messageType &&
          jsonEqual(jsonResponse, other.jsonResponse) &&
          listEqual(artifacts, other.artifacts);

  @override
  int get hashCode =>
      id.hashCode ^
      taskId.hashCode ^
      message.hashCode ^
      timestamp.hashCode ^
      messageType.hashCode ^
      jsonResponse.hashCode ^
      artifacts.hashCode;

  @override
  String toString() =>
      'Chat(id: $id, taskId: $taskId, message: $message, timestamp: $timestamp
