import 'package:auto_gpt_flutter_client/constants/app_colors.dart';
import 'package:auto_gpt_flutter_client/utils/uri_utility.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LeaderboardSubmissionDialog extends StatelessWidget {
  final Function(String, String, String)? onSubmit;

  const LeaderboardSubmissionDialog({
    Key? key,
    this.onSubmit,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8.0),
      ),
      child: Container(
        width: 260,
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Leaderboard Submission',
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: Colors.black,
                  fontSize: 16,
                  fontFamily: 'Archivo',
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(height: 14),
              const TeamNameField(),
              const SizedBox(height: 8),
              const GithubRepoUrlField(),
              const SizedBox(height: 8),
              const CommitShaField(),
              const SizedBox(height: 14),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const CancelButton(),
                  SizedBox(width: 8),
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.primaryLight,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(8.0),
                      ),
                    ),
                    onPressed: () => context.read<LeaderboardSubmissionViewModel>().validateAndSubmit,
                    child: const Text(
                      'Submit',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 12.50,
                        fontFamily: 'Archivo',
                        fontWeight: FontWeight.w400,
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class TeamNameField extends StatelessWidget {
  const TeamNameField({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final viewModel = context.watch<LeaderboardSubmissionViewModel>();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Team Name'),
        TextField(
          controller: viewModel.teamNameController,
          decoration: InputDecoration(
            hintText: 'Keyboard Warriors',
            errorText: viewModel.teamNameError,
            border: OutlineInputBorder(
              borderSide: BorderSide(
                color: viewModel.teamNameError != null ? Colors.red : Colors.grey,
              ),
            ),
          ),
        ),
      ],
    );
  }
}

class GithubRepoUrlField extends StatelessWidget {
  const GithubRepoUrlField({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final viewModel = context.watch<LeaderboardSubmissionViewModel>();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Github Repo URL'),
        TextField(
          controller: viewModel.repoUrlController,
          decoration: InputDecoration(
            hintText: 'https://github.com/KeyboardWarriors/BestAgentEver',
            errorText: viewModel.repoUrlError,
            border: OutlineInputBorder(
              borderSide: BorderSide(
                color: viewModel.repoUrlError != null ? Colors.red : Colors.grey,
              ),
            ),
          ),
        ),
      ],
    );
  }
}

class CommitShaField extends StatelessWidget {
  const CommitShaField({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final viewModel = context.watch<LeaderboardSubmissionViewModel>();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Commit SHA'),
        TextField(
          controller: viewModel.commitShaController,
          decoration: InputDecoration(
            hintText: '389131f2ab78c2cc5bdd2ec257be2d18b3a63da3',
            errorText: viewModel.commitShaError,
            border: OutlineInputBorder(
              borderSide: BorderSide(
                color: viewModel.commitShaError != null ? Colors.red : Colors.grey,
              ),
            ),
          ),
        ),
      ],
    );
  }
}

class CancelButton extends StatelessWidget {
  const CancelButton({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 106,
      height: 28,
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          backgroundColor: Colors.grey,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular
