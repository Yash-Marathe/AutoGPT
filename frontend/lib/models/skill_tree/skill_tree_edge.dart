import 'dart:convert';
import 'package:json_annotation/json_annotation.dart';

part 'skill_tree_edge.g.dart';

@JsonSerializable()
class SkillTreeEdge {
  @JsonKey(name: 'id')
  final String? id;

  @JsonKey(name: 'from')
  final String? from;

  @JsonKey(name: 'to')
  final String? to;

  @JsonKey(name: 'arrows')
  final String? arrows;

  SkillTreeEdge({
    this.id,
    this.from,
    this.to,
    this.arrows,
  });

  factory SkillTreeEdge.fromJson(Map<String, dynamic> json) =>
      _$SkillTreeEdgeFromJson(json);

  Map<String, dynamic> toJson() => _$SkillTreeEdgeToJson(this);
}


flutter pub run build_runner build
