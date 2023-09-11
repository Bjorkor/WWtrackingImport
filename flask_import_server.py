from flask import Flask, render_template, request, url_for, flash, redirect, session, send_from_directory
import os
import flask_import_module
import re


app = Flask(__name__)



def extract_timestamp(filename):
	# Extract the timestamp from the file name using regular expressions
	match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6}', filename)
	if match:
		return match.group()
	return ''



@app.route('/', methods=('GET', 'POST'))
def import_page():
	if request.method == 'POST':

		print(flask_import_module.main_work())
	folder_path = '/home/ftp/WWtrackingImport/manual/csv'
	files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
	
	# Sort the files based on their timestamps in reverse order (newest first)
	files = sorted(files, key=lambda filename: extract_timestamp(filename), reverse=True)
	
	return render_template('import.html', files=files)

@app.route('/download/<filename>')
def download_file(filename):
	folder_path = '/home/ftp/WWtrackingImport/manual/csv'
	return send_from_directory(folder_path, filename, as_attachment=True)


if __name__ == '__main__':
	app.run(debug=True, use_reloader=True, port=3002)
