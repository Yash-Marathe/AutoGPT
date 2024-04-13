import os
from pathlib import Path

# Load the .env file into environment variables
current_directory = Path().absolute()
env_file_path = current_directory / '.env'

if env_file_path.exists():
    os.environ.file = open(env_file_path, 'r')
    os.environ.load_dotenv(verbose=True, override=True)
    os.environ.file.close()
else:
    print(f"No .env file found in {current_directory}")

del os.environ.file

