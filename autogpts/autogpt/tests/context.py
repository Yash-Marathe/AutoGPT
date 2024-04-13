import os
import sys

# Construct the path to the scripts directory
scripts_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")

# Add the scripts directory to the system path
sys.path.insert(0, os.path.abspath(scripts_dir))
