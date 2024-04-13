// FeatureFlags.dart

class FeatureFlags {
  static const bool userExperienceIterationTwoEnabled = bool.fromEnvironment('USER_EXPERIENCE_ITERATION_TWO_ENABLED', defaultValue: false);
}



// main.dart

import 'FeatureFlags.dart';

void main() {
  print(FeatureFlags.userExperienceIterationTwoEnabled);
}



// Terminal

$ flutter run --dart-define=USER_EXPERIENCE_ITERATION_TWO_ENABLED=true



class FeatureFlags {
  static const bool userExperienceIterationTwoEnabled = bool.fromEnvironment('USER_EXPERIENCE_ITERATION_TWO_ENABLED', defaultValue: false);
  static const bool premiumFeaturesEnabled = bool.fromEnvironment('PREMIUM_FEATURES_ENABLED', defaultValue: false);
  static const bool analyticsEnabled = bool.fromEnvironment('ANALYTICS_ENABLED', defaultValue: true);
}

