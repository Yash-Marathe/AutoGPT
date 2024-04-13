#!/bin/bash

# Check if Flutter is installed
if ! command -v flutter &> /dev/null
then
    echo "Flutter is not installed. Please install Flutter before running this script."
    exit 1
fi

# Check if the current working directory is a Flutter project
if [ ! -d ios ] || [ ! -d android ] || [ ! -d web ] || [ ! -f pubspec.yaml ]; then
    echo "This does not appear to be a Flutter project directory. Please run this script from the root of your Flutter project."
    exit 1
fi

# Build the web app with the specified base href
flutter build web --base-href /app/ || {
    echo "Flutter build failed. Please check the output above for any errors."
    exit 1
}

echo "Flutter web app built successfully with base href /app/."
