"""
This is a minimal file intended to be run by users to help them manage the autogpt projects.

If you want to contribute, please use only libraries that come as part of Python.
To ensure efficiency, add the imports to the functions so only what is needed is imported.
"""
import os
import subprocess
import click
from github import Github

def install_dependencies():
    """Installs dependencies needed for your system. Works with Linux, MacOS and Windows WSL."""
    click.echo(
        click.style(
            """
       d8888          888             .d8888b.  8888888b. 88888888888 
      d88888          888            d88P  Y88b 888   Y88b    888     
     d88P888          8
