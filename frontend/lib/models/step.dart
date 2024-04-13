// TODO: Refactor this to match which values are required and optional
import 'package:auto_gpt_flutter_client/models/artifact.dart';

class Step {
  final String input;
  final Map<String, dynamic> _additionalInput;
  final String taskId;
  final String stepId;
  final String name;
  final String status;
  String _output;
  final Map<String, dynamic> _additionalOutput;
  final List<Artifact> _artifacts;
  final bool isLast;

  Step({
    required this.input,
    Map<String, dynamic>? additionalInput,
    required this.taskId,
    required this.stepId,
    required this.name,
    required this.status,
    String output = '',
    Map<String, dynamic>? additionalOutput,
    List<Artifact>? artifacts,
    this.isLast = false,
  })  : _additionalInput = additionalInput ?? {},
        _output = output,
        _additionalOutput = additionalOutput ?? {},
        _artifacts = artifacts ?? [];

  factory Step.fromMap(Map<String, dynamic>? map) {
    if (map == null) {
      throw ArgumentError('Null map provided to Step.fromMap');
    }
    return Step(
      input: map['input'] ?? '',
      additionalInput: map['additional_input'] != null
          ? Map<String, dynamic>.from(map['additional_input'])
          : {},
      taskId: map['task_id'] ?? '',
      stepId: map['step_id'] ?? '',
      name: map['name'] ?? '',
      status: map['status'] ?? '',
      output: map['output'] ?? '',
      additionalOutput: map['additional_output'] != null
          ? Map<String, dynamic>.from(map['additional_output'])
          : {},
      artifacts: (map['artifacts'] as List)
          .map(
              (artifact) => Artifact.fromJson(artifact as Map<String, dynamic>))
          .toList(),
      isLast: map['is_last'] ?? false,
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'input': input,
      'additional_input': _additionalInput,
      'task_id': taskId,
      'step_id': stepId,
      'name': name,
      'status': status,
      'output': _output,
      'additional_output': _additionalOutput,
     
