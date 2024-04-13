import 'dart:convert';

class Metrics {
  final String difficulty;
  final bool? success;
  final bool attempted;
  final double successPercentage;
  final int? costResources;
  final double? costTime;
  final String runTime;

  Metrics({
    required this.difficulty,
    required this.success,
    required this.attempted,
    required this.successPercentage,
    this.costResources,
    this.costTime,
    required this.runTime,
  }) : assert((costResources == null) != (costTime == null));

  factory Metrics.fromJson(Map<String, dynamic> json) {
    final success = json['success'] as bool?;
    final costResources = json['cost_resources'] as int?;
    final costTime = json['cost_time'] as double?;

    return Metrics(
      difficulty: json['difficulty'] ?? 'placeholder',
      success: success,
      attempted: json['attempted'] ?? false,
      successPercentage: (json['success_percentage'] != null)
          ? json['success_percentage'].toDouble()
          : 0.0,
      costResources: costResources,
      costTime: costTime,
      runTime: json['run_time'] ?? 'placeholder',
    );
  }

  Map<String, dynamic> toJson() => {
        'difficulty': difficulty,
        'success': success,
        'attempted': attempted,
        'success_percentage': successPercentage,
        'cost_resources': costResources,
        'cost_time': costTime,
        'run_time': runTime,
      };
}

void main() {
  final jsonString = '{"difficulty": "easy", "success": true, "attempted": true, "success_percentage": 90, "cost_resources": 10, "cost_time": 0.5, "run_time": "00:01:30"}';
  final jsonMap = json.decode(jsonString);
  final metrics = Metrics.fromJson(jsonMap);

  print('Difficulty: ${metrics.difficulty}');
  print('Success: ${metrics.success}');
  print('Attempted: ${metrics.attempted}');
  print('Success Percentage: ${metrics.successPercentage}');
  print('Cost Resources: ${metrics.costResources}');
  print('Cost Time: ${metrics.costTime}');
  print('Run Time: ${metrics.runTime}');
}
