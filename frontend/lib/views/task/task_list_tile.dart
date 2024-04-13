import 'package:flutter/material.dart';
import 'package:auto_gpt_flutter_client/models/task.dart';

class TaskListTile extends StatelessWidget {
  final Task task;
  final VoidCallback onTap;
  final VoidCallback onDelete;
  final bool selected;

  const TaskListTile({
    Key? key,
    required this.task,
    required this.onTap,
    required this.onDelete,
    this.selected = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    double tileWidth = MediaQuery.of(context).size.width - 40;
    if (tileWidth > 260) {
      tileWidth = 260;
    }

    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: tileWidth,
        height: 50,
        decoration: BoxDecoration(
          color: selected ? Colors.grey[300] : Colors.white,
          borderRadius: BorderRadius.circular(8.0),
        ),
        child: Row(
          children: [
            const SizedBox(width: 8),
            const Icon(Icons.messenger_outline, color: Colors.black),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                task.title,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(color: Colors.black),
              ),
            ),
            if (selected)
              IconButton(
                splashRadius: 0.1,
                icon: const Icon(Icons.close, color: Colors.black),
                onPressed: onDelete,
              ),
          ],
        ),
      ),
    );
  }
}
