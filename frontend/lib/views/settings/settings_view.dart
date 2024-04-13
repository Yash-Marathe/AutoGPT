import 'package:auto_gpt_flutter_client/viewmodels/settings_viewmodel.dart';
import 'package:flutter/material.dart';

class SettingsView extends StatefulWidget {
  final SettingsViewModel viewModel;

  const SettingsView({Key? key, required this.viewModel}) : super(key: key);

  @override
  _SettingsViewState createState() => _SettingsViewState();
}

class _SettingsViewState extends State<SettingsView> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.grey,
        foregroundColor: Colors.black,
        title: const Text('Settings'),
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Dark Mode Toggle
              SwitchListTile(
                title: const Text('Dark Mode'),
                value: widget.viewModel.isDarkModeEnabled,
                onChanged: widget.viewModel.toggleDarkMode,
              ),
              const Divider(),
              // Developer Mode Toggle
              SwitchListTile(
                title: const Text('Developer Mode'),
                value: widget.viewModel.isDeveloperModeEnabled,
                onChanged: widget.viewModel.toggleDeveloperMode,
              ),
              const Divider(),
              // Base URL Configuration
              const Text(
                'Agent Base URL',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              ApiBaseUrlField(),
              const Divider(),
              // Continuous Mode Steps Configuration
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    'Continuous Mode Steps',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  Row(
                    children: [
                      IconButton(
                        icon: const Icon(Icons.remove),
                        onPressed: widget.viewModel.decrementContinuousModeSteps,
                      ),
                      Text('${widget.viewModel.continuousModeSteps} Steps'),
                      IconButton(
                        icon: const Icon(Icons.add),
                        onPressed: widget.viewModel.incrementContinuousModeSteps,
                      ),
                    ],
                  ),
                ],
              ),
              const Divider(),
              // Sign out button
              ElevatedButton.icon(
                icon: const Icon(Icons.logout, color: Colors.black),
                label: const Text('Sign Out', style: TextStyle(color: Colors.black)),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.white,
                ),
                onPressed: widget.viewModel.signOut,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
