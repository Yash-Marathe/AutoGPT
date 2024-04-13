import 'package:auto_gpt_flutter_client/constants/app_colors.dart';
import 'package:flutter/material.dart';

class ContinuousModeDialog extends StatefulWidget {
  final VoidCallback? onProceed;
  final ValueChanged<bool>? onCheckboxChanged;
  final String title;
  final String description;
  final String proceedButtonText;
  final String cancelButtonText;

  const ContinuousModeDialog({
    Key? key,
    this.onProceed,
    this.onCheckboxChanged,
    this.title = 'Continuous Mode',
    this this.description = 'Agents operating in Continuous Mode will perform Actions without requesting authorization from the user. Configure the number of steps in the settings menu.',
    this.proceedButtonText = 'Proceed',
    this.cancelButtonText = 'Cancel',
  }) : super(key: key);

  @override
  _ContinuousModeDialogState createState() => _ContinuousModeDialogState();
}

class _ContinuousModeDialogState extends State<ContinuousModeDialog> {
  bool _attemptedToDismiss = false;
  bool _checkboxValue = false;

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async {
        setState(() {
          _attemptedToDismiss = true;
        });
        return false;
      },
      child: Dialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8.0),
          side: BorderSide(
            color: _attemptedToDismiss
                ? AppColors.accentDeniedLight
                : Colors.transparent,
            width: 3.0,
          ),
        ),
        child: Container(
          width: 260,
          height: 251,
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              // Black circle exclamation icon
              Icon(Icons.error_outline,
                  color: _attemptedToDismiss
                      ? AppColors.accentDeniedLight
                      : Colors.black),
              const SizedBox(height: 8),
              // Title
              Text(
                widget.title,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  color: Colors.black,
                  fontSize: 16,
                  fontFamily: 'Archivo',
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(height: 8),
              // Block of text
              SizedBox(
                width: 220,
                child: Text(
                  widget.description,
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    color: Colors.black,
                    fontSize: 12.50,
                    fontFamily: 'Archivo',
                    fontWeight: FontWeight.w400,
                  ),
                ),
              ),
              const SizedBox(height: 14),
              // Buttons
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  // Cancel Button
                  SizedBox(
                    width: 106,
                    height: 28,
                    child: ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.grey,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8.0),
                        ),
                      ),
                      onPressed: () => Navigator.of(context).pop(),
                      child: Text(
                        widget.cancelButtonText,
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 12.50,
                          fontFamily: 'Archivo',
                          fontWeight: FontWeight.w400,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  // Proceed Button
                  SizedBox(
                    width: 106,
                    height: 28,
                    child: ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.primaryLight,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8.0),
                        ),
                      ),
                      onPressed: widget.onProceed, // Use the provided callback
                      child: Text(
                        widget.proceedButtonText,
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 12.50,
                          fontFamily: 'Archivo',
                          fontWeight: FontWeight.w400,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 11),
              // Checkbox and text
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Checkbox(
                    value: _checkboxValue,
                    onChanged: (bool? newValue) {
                      setState(() {
                        _checkboxValue = newValue ?? false;
                      });
                      if (widget.onCheckboxChanged != null) {
                        widget.onCheckboxChanged!(_checkboxValue);
                      }
                    },
                  ),
                  Text(
                    "Don't ask again",
                    style: const TextStyle(
                      color: Colors.black,
                      fontSize: 11,
                      fontFamily: 'Archivo',
                      fontWeight: FontWeight.w400,
                    ),
                  ),
                ],
              ),
            ],

