import 'package:auto_gpt_flutter_client/services/auth_service.dart';
import 'package:auto_gpt_flutter_client/services/shared_preferences_service.dart';
import 'package:auto_gpt_flutter_client/utils/rest_api_utility.dart';
import 'package:flutter/material.dart';

class SettingsViewModel extends ChangeNotifier {
  bool _isDarkModeEnabled;
  bool _isDeveloperModeEnabled;
  String _baseURL;
  int _continuousModeSteps;

  final RestApiUtility _restApiUtility;
  final SharedPreferencesService _prefsService;
  final AuthService _authService;

  SettingsViewModel(this._restApiUtility, this._prefsService, this._authService) {
    _loadPreferences();
  }

  bool get isDarkModeEnabled => _isDarkModeEnabled;
  bool get isDeveloperModeEnabled => _isDeveloperModeEnabled;
  String get baseURL => _baseURL;
  int get continuousModeSteps => _continuousModeSteps;

  Future<void> _loadPreferences() async {
    _isDarkModeEnabled = await _prefsService.getBool('isDarkModeEnabled') ?? false;
    _isDeveloperModeEnabled = await _prefsService.getBool('isDeveloperModeEnabled') ?? true;
    _baseURL = await _prefsService.getString('baseURL') ?? 'http://127.0.0.1:8000/ap/v1';
    _restApiUtility.updateBaseURL(_baseURL);
    _continuousModeSteps = await _prefsService.getInt('continuousModeSteps') ?? 10;
    notifyListeners();
  }

  Future<void> toggleDarkMode(bool value) async {
    _isDarkModeEnabled = value;
    notifyListeners();
    await _prefsService.setBool('isDarkModeEnabled', value);
  }

  Future<void> toggleDeveloperMode(bool value) async {
    _isDeveloperModeEnabled = value;
    notifyListeners();
    await _prefsService.setBool('isDeveloperModeEnabled', value);
  }

  Future<void> updateBaseURL(String value) async {
    _baseURL = value;
    notifyListeners();
    await _prefsService.setString('baseURL', value);
    _restApiUtility.updateBaseURL(value);
  }

  Future<void> updateContinuousModeSteps(int value) async {
    _continuousModeSteps = value;
    notifyListeners();
    await _prefsService.setInt('continuousModeSteps', value);
  }

  Future<void> incrementContinuousModeSteps() async {
    if (_continuousModeSteps < 100) {
      _continuousModeSteps++;
      notifyListeners();
      await _prefsService.setInt('continuousModeSteps', _continuousModeSteps);
    }
  }

  Future<void> decrementContinuousModeSteps() async {
    if (_continuousModeSteps > 1) {
      _continuousModeSteps--;
      notifyListeners();
      await _prefsService.setInt('continuousModeSteps', _continuousModeSteps);
    }
  }

  Future<void> signOut() async {
    await _authService.signOut();
  }
}
