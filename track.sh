#!/bin/sh

# send start tick to cronitor
curl https://cronitor.link/p/e12853e7180849b99497cbf55f5b8859/kTj0MO?state=run

# Set the path to your virtual environment directory
VENV_DIR="/home/ftp/WWtrackingImport/venv"

# Set the path to your Python script
PYTHON_SCRIPT="/home/ftp/WWtrackingImport/app.py"

# Activate the virtual environment
. "$VENV_DIR/bin/activate"

# Execute the Python script
python "$PYTHON_SCRIPT"


# check for success
if [ $? == 0 ]
then
        # if success, report success to cronitor
        curl https://cronitor.link/p/e12853e7180849b99497cbf55f5b8859/kTj0MO?state=complete
else
        # if fail, report failure to cronitor
        curl https://cronitor.link/p/e12853e7180849b99497cbf55f5b8859/kTj0MO?state=fail
fi

# Deactivate the virtual environment
deactivate

