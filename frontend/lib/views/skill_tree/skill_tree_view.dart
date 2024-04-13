import 'package:auto_gpt_flutter_client/models/skill_tree/skill_tree_category.dart';
import 'package:auto_gpt_flutter_client/models/skill_tree/skill_tree_node.dart';
import 'package:auto_gpt_flutter_client/viewmodels/skill_tree_viewmodel.dart';
import 'package:auto_gpt_flutter_client/views/skill_tree/tree_node_view.dart';
import 'package:flutter/material.dart';
import 'package:graphview/GraphView.dart';

class SkillTreeView extends StatefulWidget {
  final SkillTreeViewModel viewModel;

  const SkillTreeView({Key? key, required this.viewModel}) : super(key: key);

  @override
  _SkillTreeViewState createState() => _SkillTreeViewState();
}

class _SkillTreeViewState extends State<SkillTreeView> {
  Future<void>? _initialization;

  @override
  void initState() {
    super.initState();
    _initialization = widget.viewModel.initializeSkillTree();
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        FutureBuilder<void>(
          future: _initialization,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            }

            if (snapshot.hasError) {
              return const Center(child: Text("An error occurred"));
            }

            return Scaffold(
              body: Column(
                mainAxisSize: MainAxisSize.max,
                children: [
                  Expanded(
                    child: _SkillTreeGraph(),
                  ),
                ],
              ),
              floatingActionButton: FloatingActionButton(
                onPressed: () {
                  setState(() {
                    _initialization = widget.viewModel.initializeSkillTree();
                  });
                },
                child: const Icon(Icons.refresh),
              ),
            );
          },
        ),
        Positioned(
          top: 10,
          left: 10,
          child: Material(
            type: MaterialType.transparency,
            child: DropdownButton<SkillTreeCategory>(
              value: widget.viewModel.currentSkillTreeType,
              items: SkillTreeCategory.values.map((category) {
                return DropdownMenuItem<SkillTreeCategory>(
                  value: category,
                  child: Text(category.stringValue),
                );
              }).toList(),
              onChanged: (newValue) {
                if (newValue != null) {
                  setState(() {
                    widget.viewModel.currentSkillTreeType = newValue;
                    _initialization = widget.viewModel.initializeSkillTree();
                  });
                }
              },
            ),
          ),
        )
      ],
    );
  }
}

class _SkillTreeGraph extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final viewModel = SkillTreeViewModel.of(context);

    // Create Node and Edge objects for GraphView
    final nodeMap = <String, Node>{};
    for (final skillTreeNode in viewModel.skillTreeNodes) {
      final node = Node.Id(skillTreeNode.id);
      viewModel.graph.addNode(node);
      nodeMap[skillTreeNode.id] = node;
    }

    for (final skillTreeEdge in viewModel.skillTreeEdges) {
      final fromNode = nodeMap[skillTreeEdge.from];
      final toNode = nodeMap[skillTreeEdge.to];
      if (fromNode != null && toNode != null) {
        viewModel.graph.addEdge(fromNode, toNode);
      }
    }

    return InteractiveViewer(
      constrained: false,
      child: SizedBox(
        width: MediaQuery.of(context).size.width,
        height: MediaQuery.of(context).size.height,
        child: Align(
          alignment: Alignment.centerLeft,
          child: GraphView(
            graph: viewModel.graph,
            algorithm: SugiyamaAlgorithm(viewModel.builder),
            paint: Paint()
              ..color = Colors.green
              ..strokeWidth = 1
              ..style = PaintingStyle.stroke,
            builder: (Node node) {
              final nodeId = node.key?.value as String;
              final skillTreeNode = viewModel.getNodeById(nodeId);
              if (skillTreeNode != null) {
                return TreeNodeView(
                  node: skillTreeNode,
                  selected: nodeId == viewModel.selectedNode?.id,
                );
              } else {
                return const SizedBox(); // Return an empty widget if the node is not found
              }
            },
          ),
        ),
      ),
    );
  }
}
