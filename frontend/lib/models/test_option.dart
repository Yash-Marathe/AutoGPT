/// `TestOption` is an enumeration of the available test options that can be selected in the skill tree view.
///
/// Each value of this enum represents a distinct test option that can be executed.
enum TestOption {
  /// Represents the option to run a single test.
  runSingleTest,

  /// Represents the option to run a test suite including the selected node and its ancestors.
  runTestSuiteIncludingSelectedNodeAndAncestors,

  /// Represents the option to run all tests in a category.
  runAllTestsInCategory,
}

/// An extension on the `TestOption` enum to provide a string representation for each test option.
///
/// This extension adds a `description` getter on `TestOption` to easily retrieve the human-readable
/// string associated with each option. This is particularly helpful for UI display purposes.
extension TestOptionExtension on TestOption {
  /// Gets the string representation of the test option.
  ///
  /// Returns a human-readable string that describes the test option. This string is intended
  /// to be displayed in the UI for user selection.
  String get description {
    return describeEnum(this);
  }

  /// Converts a [description] string to its corresponding [TestOption] enum value.
  ///
  /// This method is helpful for converting string representations of test options
  /// received from various sources (like user input or server responses) into
  /// their type-safe enum equivalents.
  ///
  /// Returns the matching [TestOption] enum value if found, otherwise returns `null`.
  static TestOption? fromDescription(String description) {
    return TestOption.values.firstWhereOrNull((option) => option.description == description);
  }
}
