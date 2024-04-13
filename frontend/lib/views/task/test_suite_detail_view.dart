import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class TaskListTile extends StatefulWidget {
  final String id;
  final String title;
  final bool completed;
  final Function(String) onTap;
  final Function(String) onDelete;
  final Function(String, bool) onChanged;
  final bool selected;

  const TaskListTile({
    Key? key,
    required this.id,
    required this.title,
    required this.completed,
    required this.onTap,
    required this.onDelete,
    required this.onChanged,
    required this.selected,
  }) : super(key: key);

  @override
  _TaskListTileState createState() => _TaskListTileState();
}

class _TaskListTileState extends State<TaskListTile> {
  bool _checked = false;

  @override
  void initState() {
    super.initState();
    _checked = widget.completed;
  }

  @override
  Widget build(BuildContext context) {
    return ListTile(
      key: ValueKey(widget.id),
      leading: Checkbox(
        value: _checked,
        onChanged: (value) {
          setState(() {
            _checked = value!;
          });
          widget.onChanged(widget.id, _checked);
        },
      ),
      title: Text(widget.title),
      trailing: SizedBox(
        width: 100,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            IconButton(
              icon: Icon(Icons.delete),
              onPressed: () {
                widget.onDelete(widget.id);
              },
            ),
            Consumer<ChatViewModel>(
              builder: (context, chatViewModel, child) {
                return Visibility(
                  visible: widget.id == chatViewModel.currentTaskId,
                  child: IconButton(
                    icon: Icon(Icons.clear),
                    onPressed: () {
                      chatViewModel.clearCurrentTaskAndChats();
                    },
                  ),
                );
              },
            ),
          ],
        ),
      ),
      onTap: () {
        widget.onTap(widget.id);
      },
      selected: widget.selected,
    );
  }
}


import 'package:auto_gpt_flutter_client/models/test_suite.dart';
import 'package:auto_gpt_flutter_client/viewmodels/chat_viewmodel.dart';
import 'package:auto_gpt_flutter_client/viewmodels/task_viewmodel.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class TestSuiteDetailView extends StatefulWidget {
  final TaskViewModel viewModel;
  final TestSuite testSuite;

  const TestSuiteDetailView({
    Key? key,
    required this.testSuite,
    required this.viewModel,
  }) : super(key: key);

  @override
  _TestSuiteDetailViewState createState() => _TestSuiteDetailViewState();
}

class _TestSuiteDetailViewState extends State<TestSuiteDetailView> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.grey,
        foregroundColor: Colors.black,
        title: Text("${widget.testSuite.timestamp}"),
        leading: IconButton(
          icon: Icon(Icons.arrow_back),
          onPressed: () => widget.viewModel.deselectTestSuite(),
        ),
      ),
      body: Column(
        children: [
          // Task List
          Expanded(
            child: ListView.builder(
              itemCount: widget.testSuite.tests.length,
              itemBuilder: (context, index) {
                final task = widget.testSuite.tests[index];
                return Cons
