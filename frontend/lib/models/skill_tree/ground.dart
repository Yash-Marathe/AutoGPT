class Ground {
  final String answer;
  final List<String> shouldContain;
  final List<String> shouldNotContain;
  final List<String> files;
  final Map<String, dynamic> eval;

  Ground({
    required this.answer,
    required List<String> shouldContain,
    required List<String> shouldNotContain,
    required List<String> files,
    required Map<String, dynamic> eval,
  })  : shouldContain = shouldContain.isNotEmpty ? shouldContain : [],
        shouldNotContain = shouldNotContain.isNotEmpty ? shouldNotContain : [],
        files = files.isNotEmpty ? files : [];

  factory Ground.fromJson(Map<String, dynamic> json) {
    return Ground(
      answer: json['answer'] ?? "",
      shouldContain: List<String>.from(json['should_contain'] ?? []),
      shouldNotContain: List<String>.from(json['should_not_contain'] ?? []),
      files: List<String>.from(json['files'] ?? []),
      eval: json['eval'] ?? {},
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'answer': answer,
      'should_contain': shouldContain,
      'should_not_contain': shouldNotContain,
      'files': files,
      'eval': eval,
    };
  }
}
