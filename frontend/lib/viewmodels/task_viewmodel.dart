import 'dart:convert';
import 'package:auto_gpt_flutter_client/models/task.dart';
import 'package:auto_gpt_flutter_client/models/test_suite.dart';
import 'package:auto_gpt_flutter_client/services/shared_preferences_service.dart';
import 'package:auto_gpt_flutter_client/services/task_service.dart';
import 'package:flutter/foundation.dart';
import 'package:collection/collection.dart';

class TaskViewModel with ChangeNotifier {
  final TaskService _taskService;
  final SharedPreferencesService _prefsService;

  List<Task> _tasks = [];
  List<TestSuite> _testSuites = [];
  List<dynamic> combinedDataSource = [];
  List<Task> tasksDataSource = [];

  Task? _selectedTask;
  TestSuite? _selectedTestSuite;

  bool _isWaitingForAgentResponse = false;

  bool get isWaitingForAgentResponse => _isWaitingForAgentResponse;

  TaskViewModel(this._taskService, this._prefsService);

  Task? get selectedTask => _selectedTask;
  TestSuite? get selectedTestSuite => _selectedTestSuite;

  Future<String> createTask(String title) async {
    _isWaitingForAgentResponse = true;
    notifyListeners();
    try {
      final newTask = TaskRequestBody(input: title);
      final createdTask = await _taskService.createTask(newTask);
      final newTaskObject =
          Task(id: createdTask['task_id'], title: createdTask['input']);

      _tasks.add(newTaskObject);
      _tasks = _tasks.reversed.toList();

      await _saveTasksToPrefs();

      final taskId = newTaskObject.id;
      print("Task $taskId created successfully!");

      return newTaskObject.id;
    } catch (e, stackTrace) {
      print('Error creating task: $e\n$stackTrace');
      rethrow;
    } finally {
      _isWaitingForAgentResponse = false;
      notifyListeners();
    }
  }

  void deleteTask(String taskId) {
    _taskService.saveDeletedTask(taskId);
    _tasks.removeWhere((task) => task.id == taskId);
    _saveTasksToPrefs();
    notifyListeners();
    print("Task $taskId deleted successfully!");
  }

  Future<void> fetchTasks() async {
    try {
      final tasksFromApi = await _taskService.fetchAllTasks();
      _tasks = tasksFromApi
          .where((task) => !_taskService.isTaskDeleted(task.id))
          .toList();

      _tasks = _tasks.reversed.toList();

      await _saveTasksToPrefs();

      notifyListeners();
      print("Tasks fetched successfully!");
    } catch (error) {
      print("Error fetching tasks: $error");
    }
  }

  void selectTask(String id) {
    final task = _tasks.firstWhereOrNull((t) => t.id == id);

    if (task != null) {
      _selectedTask = task;
      print("Selected task with ID: ${task.id} and Title: ${task.title}");
      notifyListeners(); // Notify listeners to rebuild UI
    } else {
      final errorMessage =
          "Error: Attempted to select a task with ID: $id that does not exist in the data source.";
      print(errorMessage);
      throw ArgumentError(errorMessage);
    }
  }

  void deselectTask() {
    _selectedTask = null;
    print("Deselected the current task.");
    notifyListeners(); // Notify listeners to rebuild UI
  }

  void selectTestSuite(TestSuite testSuite) {
    _selectedTestSuite = testSuite;
    notifyListeners();
  }

  void deselectTestSuite() {
    _selectedTestSuite = null;
    notifyListeners();
  }

  Future<void> _saveTasksToPrefs() async {
    final tasksToStore = _tasks.map((task) => jsonEncode(task.toJson())).toList();
    await _prefsService.setStringList('tasks', tasksToStore);
  }

  Future<void> _saveTestSuitesToPrefs() async {
    final testSuitesToStore =
        _testSuites.map((testSuite) => jsonEncode(testSuite.toJson())).toList();
    await _prefsService.setStringList('testSuites', testSuitesToStore);
  }

  Future<void> fetchTestSuites() async {
    final storedTestSuites =
        await _prefsService.getStringList('testSuites') ?? [];
    _testSuites = storedTestSuites
        .map((testSuiteMap) => TestSuite.fromJson(jsonDecode(testSuiteMap)))
        .toList();
    notifyListeners();
  }

  Future<void> combineData() async {
    await fetchTasks();
    await fetchTestSuites();

    combinedDataSource.clear();
    tasksDataSource.clear();

    Map<String, TestSuite> testSuiteMap = {};

    for (var task in _tasks) {
      bool found = false;

      for (var testSuite in _testSuites) {
        if (testSuite.tests.contains(task)) {
          found = true;

          if (testSuiteMap.containsKey(testSuite.timestamp)) {
            testSuiteMap[testSuite.timestamp]!.tests.add(task);
          } else {
            final newTestSuite = TestSuite(
              timestamp: testSuite.timestamp,
              tests: [task],
            );
            testSuiteMap[testSuite.timestamp] = newTestSuite;
            combinedDataSource.add(newTestSuite);
          }
          break;
        }
      }

      if (!found) {
        combinedDataSource.add(task);

