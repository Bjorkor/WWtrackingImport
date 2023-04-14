#!/bin/sh

# Set the path to your virtual environment directory
VENV_DIR="/home/ftp/WWtrackingImport/venv"

# Set the path to your Python script
PYTHON_SCRIPT="/home/ftp/WWtrackingImport/autoimport.py"

# Activate the virtual environment
. "$VENV_DIR/bin/activate"

# Execute the Python script
python "$PYTHON_SCRIPT"

# Deactivate the virtual environment
deactivate