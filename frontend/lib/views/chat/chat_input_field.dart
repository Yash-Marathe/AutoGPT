import 'package:auto_gpt_flutter_client/viewmodels/chat_viewmodel.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ChatInputField extends StatefulWidget {
  // Callback to be triggered when the send button is pressed
  final Function(String) onSendPressed;
  final FocusNode focusNode;
  final TextEditingController controller;

  const ChatInputField({
    Key? key,
    required this.onSendPressed,
    required this.focusNode,
    required this.controller,
  }) : super(key: key);

  @override
  _ChatInputFieldState createState() => _ChatInputFieldState();
}

class _ChatInputFieldState extends State<ChatInputField> {
  final FocusNode _throwawayFocusNode = FocusNode();

  @override
  void initState() {
    super.initState();
    widget.focusNode.addListener(() {
      if (widget.focusNode.hasFocus) {
        _executeContinuousMode();
      }
    });
  }

  @override
  void dispose() {
    widget.focusNode.dispose(); // Dispose of the FocusNode when you're done.
    super.dispose();
  }

  void _executeContinuousMode() {
    widget.onSendPressed(widget.controller.text);
    widget.controller.clear();
    widget.focusNode.unfocus();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      constraints: const BoxConstraints(
        minHeight: 50,
        maxHeight: 400,
      ),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border.all(color: Colors.black, width: 0.5),
        borderRadius: BorderRadius.circular(8),
      ),
      padding: const EdgeInsets.symmetric(horizontal: 8),
      child: SingleChildScrollView(
        reverse: true,
        child: TextField(
          controller: widget.controller,
          focusNode: widget.focusNode,
          maxLines: null,
          decoration: InputDecoration(
            hintText: 'Type a message...',
            border: InputBorder.none,
            suffixIcon: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Tooltip(
                  message: 'Send a single message',
                  child: IconButton(
                    splashRadius: 0.1,
                    icon: const Icon(Icons.send),
                    onPressed: () {
                      widget.onSendPressed(widget.controller.text);
                      widget.controller.clear();
                    },
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class ChatInputFieldWithContinuousMode extends StatefulWidget {
  // Callback to be triggered when the send button is pressed
  final Function(String) onSendPressed;
  final ChatViewModel viewModel;
  final Function() onContinuousModePressed;

  const ChatInputFieldWithContinuousMode({
    Key? key,
    required this.onSendPressed,
    required this.viewModel,
    required this.onContinuousModePressed,
  }) : super(key: key);

  @override
  _ChatInputFieldWithContinuousModeState createState() =>
      _ChatInputFieldWithContinuousModeState();
}

class _ChatInputFieldWithContinuousModeState
    extends State<ChatInputFieldWithContinuousMode> {
  late final FocusNode _focusNode;
  late final TextEditingController _controller;
  bool _isContinuousMode = false;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _controller = TextEditingController();
    _focusNode.addListener(() {
      if (_focusNode.hasFocus) {
        widget.onContinuousModePressed();
      }
    });
  }

  @override
  void dispose() {
    _focusNode.dispose();
    _controller.dispose();
    super.dispose();
  }

  Future<void> _presentContinuousModeDialogIfNeeded() async {
    final showContinuousModeDialog =
        await widget.viewModel.prefsService.getBool('showContinuousModeDialog') ??
            true;

    FocusScope.of(context).requestFocus(_throwawayFocusNode);
    if (showContinuousModeDialog) {
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return ContinuousModeDialog(
            onProceed: () {
              Navigator.of(context).pop();
              _executeContinuousMode();
            },
            onCheckboxChanged: (bool value) async {
              await widget.viewModel.prefsService
                  .setBool('showContinuousModeDialog', !value);
            },
          );
        },
      );
    } else {
      _executeContinuousMode();
    }
  }

  void _executeContinuousMode() {
    setState(() {
      _isContinuousMode = true;
    });
    widget.onContinuousModePressed();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        ChatInputField(
          onSendPressed: widget.onSendPressed,
          focusNode: _focusNode,
          controller: _controller,
        ),
        if (!_isContinuousMode)
          ElevatedButton(
            onPressed: () {
              _presentContinuousModeDialogIfNeeded();
            },
            child: const Text('Enable continuous mode'),
          ),
      ],
    );
  }
}
