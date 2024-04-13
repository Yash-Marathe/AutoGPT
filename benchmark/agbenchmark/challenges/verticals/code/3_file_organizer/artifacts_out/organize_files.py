import argparse
import os
import shutil


def organize_files(directory_path):
    # Define file type groups
    file_types = {
        "images": [".png", ".jpg", ".jpeg"],
        "documents": [".pdf", ".docx", ".txt"],
        "audio": [".mp3", ".wav", ".flac"],
    }

    # Create the folders if they don't exist
    for folder_name, extensions in file_types.items():
        folder_path = os.path.join(directory_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)

    # Traverse through all files and folders in the specified directory
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            # Get file extension
            _, file_extension = os.path.splitext(file)

            # Skip directories
            if os.path.isdir(os.path.join(root, file)):
                continue

            # Move files to corresponding folders
            for folder_name, extensions in file_types.items():
                if file_extension in extensions:
                    old_path = os.path.join(root, file)
                    new_path = os.path.join(directory_path, folder_name, file)
                    if old_path != new_path:
                        shutil.move(old_path, new_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Organize files in a directory based on their file types"
    )
    parser.add_argument(
        "-d",
        "--directory_path",
        type=str,
        required=True,
        help="The path of the directory to be organized",
    )

    args = parser.parse_args()

    organize_files(args.directory_path)
