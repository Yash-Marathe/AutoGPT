// TODO: Consider using a more descriptive name for the enum
// TODO: Consider adding a description for each enum value

/// <summary>
/// Represents the status of a benchmark task.
/// </summary>
public enum BenchmarkTaskStatus
{
    /// <summary>
    /// The benchmark task has not yet started.
    /// </summary>
    NotStarted,

    /// <summary>
    /// The benchmark task is currently in progress.
    /// </summary>
    InProgress,

    /// <summary>
    /// The benchmark task has completed successfully.
    /// </summary>
    Success,

    /// <summary>
    /// The benchmark task has completed with an error or failure.
    /// </summary>
    Failure
}
