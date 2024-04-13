class Info {
  final String difficulty;
  final String description;
  final List<String> sideEffects;

  Info({
    required this.difficulty,
    required this.description,
    List<String> sideEffects = const [],
  }) : sideEffects = sideEffects.where((effect) => effect != null).toList();

  factory Info.fromJson(Map<String, dynamic> json) {
    return Info(
      difficulty: json['difficulty'] ?? "",
      description: json['description'] ?? "",
      sideEffects: (json['side_effects'] as List?)?.where((effect) => effect != null)?.map((effect) => effect.toString())?.toList() ?? const [],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'difficulty': difficulty,
      'description': description,
      'side_effects': sideEffects,
    };
  }
}

