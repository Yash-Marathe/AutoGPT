class RepositoryInfo {
  final String repoUrl;
  final String teamName;
  final String benchmarkGitCommitSha;
  final String agentGitCommitSha;

  RepositoryInfo({
    required this.repoUrl,
    required this.teamName,
    required this.benchmarkGitCommitSha,
    required this.agentGitCommitSha,
  });

  factory RepositoryInfo.fromJson(Map<String, dynamic> json) => RepositoryInfo(
        repoUrl: json['repo_url'] ??
            'https://github.com/Significant-Gravitas/AutoGPT',
        teamName: json['team_name'] ?? 'placeholder',
        benchmarkGitCommitSha: json['benchmark_git_commit_sha'] ?? 'placeholder',
        agentGitCommitSha: json['agent_git_commit_sha'] ?? 'placeholder',
      );

  Map<String, dynamic> toJson() => {
        'repo_url': repoUrl,
        'team_name': teamName,
        'benchmark_git_commit_sha': benchmarkGitCommitSha,
        'agent_git_commit_sha': agentGitCommitSha,
      };
}
