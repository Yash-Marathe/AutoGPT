import 'package:auto_gpt_flutter_client/models/benchmark/benchmark_task_status.dart';
import 'package:auto_gpt_flutter_client/models/test_option.dart';
import 'package:auto_gpt_flutter_client/viewmodels/chat_viewmodel.dart';
import 'package:auto_gpt_flutter_client/viewmodels/skill_tree_viewmodel.dart';
import 'package:auto_gpt_flutter_client/viewmodels/task_queue_viewmodel.dart';
import 'package:auto_gpt_flutter_client/viewmodels/task_viewmodel.dart';
import 'package:auto_gpt_flutter_client/views/task_queue/leaderboard_submission_button.dart';
import 'package:auto_gpt_flutter_client/views/task_queue/leaderboard_submission_dialog.dart';
import 'package:auto_gpt_flutter_client/views/task_queue/test_suite_button.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class TaskQueueView extends StatelessWidget {
  final TaskQueueViewModel viewModel;

  TaskQueueView({required this.viewModel});

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.white,
      child: Column(
        children: [
          Expanded(
            child: ListView.separated(
              itemCount: viewModel.selectedNodeHierarchy?.length ?? 0,
              separatorBuilder: (context, index) => Divider(height: 1),
              itemBuilder: (context, index) {
                final node = viewModel.selectedNodeHierarchy![index];
                return _buildTaskTile(node);
              },
            ),
          ),
          _buildButtons(context),
        ],
      ),
    );
  }

  Widget _buildTaskTile(dynamic node) {
    Widget leadingWidget;
    final status = viewModel.benchmarkStatusMap[node];

    switch (status) {
      case null:
      case BenchmarkTaskStatus.notStarted:
        leadingWidget = _buildNotStartedWidget();
        break;
      case BenchmarkTaskStatus.inProgress:
        leadingWidget = _buildInProgressWidget();
        break;
      case BenchmarkTaskStatus.success:
        leadingWidget = _buildSuccessWidget();
        break;
      case BenchmarkTaskStatus.failure:
        leadingWidget = _buildFailureWidget();
        break;
    }

    return Container(
      margin: EdgeInsets.fromLTRB(20, 5, 20, 5),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border.all(color: Colors.black, width: 1),
        borderRadius: BorderRadius.circular(4),
      ),
      child: ListTile(
        leading: leadingWidget,
        title: Center(child: Text('${node.label}')),
        subtitle: Center(child: Text('${node.data.info.description}')),
      ),
    );
  }

  Widget _buildNotStartedWidget() {
    return CircleAvatar(
      radius: 12,
      backgroundColor: Colors.grey,
      child: CircleAvatar(
        radius: 6,
        backgroundColor: Colors.white,
      ),
    );
  }

  Widget _buildInProgressWidget() {
    return SizedBox(
      width: 24,
      height: 24,
      child: CircularProgressIndicator(strokeWidth: 2),
    );
  }

  Widget _buildSuccessWidget() {
    return CircleAvatar(
      radius: 12,
      backgroundColor: Colors.green,
      child: CircleAvatar(
        radius: 6,
        backgroundColor: Colors.white,
      ),
    );
  }

  Widget _buildFailureWidget() {
    return CircleAvatar(
      radius: 12,
      backgroundColor: Colors.red,
      child: CircleAvatar(
        radius: 6,
        backgroundColor: Colors.white,
      ),
    );
  }

  Widget _buildButtons(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(20),
      child: Column(
        children: [
          TestSuiteButton(
            isDisabled: viewModel.isBenchmarkRunning,
            selectedOptionString: viewModel.selectedOption.description,
            onOptionSelected: (selectedOption) {
              final skillTreeViewModel =
                  Provider.of<SkillTreeViewModel>(context, listen: false);
              viewModel.updateSelectedNodeHierarchyBasedOnOption(
                  TestOptionExtension.fromDescription(selectedOption)!,
                  skillTreeViewModel.selectedNode,
                  skillTreeViewModel.skillTreeNodes,
                  skillTreeViewModel.skillTreeEdges);
            },
            onPlayPressed: (selectedOption) {
              final chatViewModel =
                  Provider.of<ChatViewModel>(context, listen: false);
              final taskViewModel =
                  Provider.of<TaskViewModel>(context, listen: false);
              chatViewModel.clearCurrentTaskAndChats();
              viewModel.runBenchmark(chatViewModel, taskViewModel);
            },
          ),
          SizedBox(height: 8),
          LeaderboardSubmissionButton(
            onPressed: viewModel.benchmarkStatusMap.isEmpty ||
                    viewModel.isBenchmarkRunning

