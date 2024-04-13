import 'package:auto_gpt_flutter_client/models/pagination.dart';
import 'package:auto_gpt_flutter_client/models/task.dart';

class TaskResponse {
  final List<Task> tasks;
  final Pagination pagination;

  TaskResponse({required this.tasks, required this.pagination});

  factory TaskResponse.fromJson(Map<String, dynamic> json) {
    return TaskResponse(
      tasks: (json['tasks'] as List<dynamic>)
          .map((taskJson) => Task.fromMap(taskJson as Map<String, dynamic>))
          .toList(),
      pagination: Pagination.fromJson(json['pagination']),
    );
  }
}

