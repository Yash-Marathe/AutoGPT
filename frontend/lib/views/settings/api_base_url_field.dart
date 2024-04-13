import 'package:auto_gpt_flutter_client/viewmodels/settings_viewmodel.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class ApiBaseUrlField extends StatelessWidget {
  final TextEditingController _controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    final SettingsViewModel settingsViewModel = Provider.of<SettingsViewModel>(context);

    // Initialize the controller with the current base URL
    void initState() {
      super.initState();
      _controller.text = settingsViewModel.baseURL;
    }

    // Update the base URL in the view model
    void updateBaseUrl() {
      settingsViewModel.updateBaseURL(_controller.text);
    }

    // Reset the base URL to the default value
    void resetBaseUrl() {
      _controller.text = 'http://127.0.0.1:8000/ap/v1';
      updateBaseUrl();
    }

    return Column(
      children: [
        Container(
          height: 50,
          decoration: BoxDecoration(
            color: Colors.white,
            border: Border.all(color: Colors.black, width: 0.5),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8),
            child: TextField(
              controller: _controller,
              decoration: const InputDecoration(
                border: InputBorder.none,
                hintText: 'Agent Base URL',
              ),
            ),
          ),
        ),
        const SizedBox(height: 16),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            ElevatedButton(
              onPressed: resetBaseUrl,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.white,
                foregroundColor: Colors.black,
                textStyle: const TextStyle(
                  color: Colors.black,
                ),
              ),
              child: const Text("Reset"),
            ),
            ElevatedButton(
              onPressed: updateBaseUrl,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.white,
                foregroundColor: Colors.black,
                textStyle: const TextStyle(
                  color: Colors.black,
                ),
              ),
              child: const Text("Update"),
            ),
          ],
        ),
      ],
    );
  }
}
