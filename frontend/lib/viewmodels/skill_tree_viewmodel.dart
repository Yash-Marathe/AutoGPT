import 'dart:convert';
import 'dart:developer';

import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:graphview/GraphView.dart';

import 'package:auto_gpt_flutter_client/models/skill_tree/skill_tree_category.dart';
import 'package:auto_gpt_flutter_client/models/skill_tree/skill_tree_edge.dart';
import 'package:auto_gpt_flutter_client/models/skill_tree/skill_tree_node.dart';

class SkillTreeViewModel with ChangeNotifier {
  SkillTreeViewModel() {
    initializeSkillTree();
  }

  List<SkillTreeNode> _skillTreeNodes = [];
  List<SkillTreeNode> get skillTreeNodes => _skillTreeNodes;

  List<SkillTreeEdge> _skillTreeEdges = [];
  List<SkillTreeEdge> get skillTreeEdges => _skillTreeEdges;

  SkillTreeNode? _selectedNode;
  SkillTreeNode? get selectedNode => _selectedNode;

  final Graph graph = Graph();
  late SugiyamaConfiguration builder;

  SkillTreeCategory currentSkillTreeType = SkillTreeCategory.general;

  Future<void> initializeSkillTree() async {
    try {
      resetState();

      final String fileName = currentSkillTreeType.jsonFileName;
      final String jsonContent = await _loadAsset(fileName);
      final Map<String, dynamic> decodedJson = jsonDecode(jsonContent);

      _skillTreeNodes = decodedJson['nodes']
          .map((nodeMap) => SkillTreeNode.fromJson(nodeMap))
          .toList();

      _skillTreeEdges = decodedJson['edges']
          .map((edgeMap) => SkillTreeEdge.fromJson(edgeMap))
          .toList();

      builder = _createSugiyamaConfiguration();

      notifyListeners();
    } catch (e, stackTrace) {
      log('Error initializing skill tree: $e\n$stackTrace');
    }
  }

  void resetState() {
    _skillTreeNodes = [];
    _skillTreeEdges = [];
    _selectedNode = null;
  }

  void toggleNodeSelection(String nodeId) {
    if (_selectedNode?.id == nodeId) {
      _selectedNode = null;
    } else {
      _selectedNode = _skillTreeNodes.firstWhere((node) => node.id == nodeId);
    }
    notifyListeners();
  }

  SkillTreeNode? getNodeById(String nodeId) {
    try {
      return _skillTreeNodes.firstWhere((node) => node.id == nodeId);
    } catch (e) {
      print("Node with ID $nodeId not found: $e");
      return null;
    }
  }

  Future<String> _loadAsset(String fileName) =>
      rootBundle.loadString('assets/$fileName');

  SugiyamaConfiguration _createSugiyamaConfiguration() {
    return SugiyamaConfiguration()
      ..orientation = SugiyamaConfiguration.ORIENTATION_LEFT_RIGHT
      ..bendPointShape = CurvedBendPointShape(curveLength: 20);
  }
}
