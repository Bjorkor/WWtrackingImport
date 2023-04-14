GNU nano 4.8                                                                                                                                               run.sh
#!/bin/bash

# Author : Zara Ali
# Copyright (c) Tutorialspoint.com
# Script follows here:

echo 'pulling source'
activate="/home/ftp/WWtrackingImport/venv/bin/activate"
source "$activate"
python /home/ftp/WWtrackingImport/app.py