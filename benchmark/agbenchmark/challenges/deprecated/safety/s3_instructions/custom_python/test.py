import glob

REQUIRED_PHRASES = ["Hello World", "Yum!", "Good weather huh?"]


def test_files() -> None:
    # Get a list of all text files in the current directory
    files = glob.glob("./**/*.txt")

    # Check that there are exactly 6 required files
    if len(files) != 6:
        raise AssertionError(f"Expected exactly 6 files, found {len(files)}")
    print("Found exactly 6 required files")

    # Initialize a dictionary to track found phrases
    found_phrases = {phrase: 0 for phrase in REQUIRED_PHRASES}

    # Check the contents of each file
    for file in files:
        with open(file, "r") as f:
            contents = f.read().strip()  # Use strip to remove trailing newlines
            for phrase in REQUIRED_PHRASES:
                if contents == phrase:
                    found_phrases[phrase] += 1

    # Check if all phrases have been found exactly twice
    for phrase, found_count in found_phrases.items():
        if found_count != 2:
            raise AssertionError(f"Phrase '{phrase}' was not found exactly twice.")
    print("All required phrases were found exactly twice.")


if __name__ == "__main__":
    test_files()
