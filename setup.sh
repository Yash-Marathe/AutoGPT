#!/usr/bin/env zsh

if [[ "$(uname)" == "Darwin" ]] || [[ "$(uname)" == "Linux" ]]; then
  if ! command -v python3 &> /dev/null; then
    echo "python3 could not be found"
    if ! command -v pyenv &> /dev/null; then
      echo "pyenv could not be found"
      curl https://pyenv.run | bash
      if ! command -v pyenv &> /dev/null; then
        echo "pyenv install failed, exiting"
        exit 1
      fi
    fi
    pyenv install 3.11.5
    pyenv global 3.11.5
  fi

  if ! command -v poetry &> /dev/null; then
    echo "poetry could not be found"
    if [[ ! -d "$HOME/.pyenv" ]]; then
      echo "pyenv root directory not found, exiting"
      exit 1
    fi
    if [[ ! -d "$HOME/.poetry" ]]; then
      curl -sSL https://install.python-poetry.org | python3
      if ! command -v poetry &> /dev/null; then
        echo "poetry install failed, exiting"
        exit 1
      fi
    fi
  fi

  if poetry --version &> /dev/null; then
    exit 0
  else
    echo "poetry install failed, exiting"
    exit 1
  fi
else
  if [[ "$OSTYPE" == "cygwin" ]] ||
