from flask import Flask, render_template, request, url_for, flash, redirect, session
import os





app = Flask(__name__)

def recallLastOrder():
    file_path = '/home/ftp/WWtrackingImport/lastorder'

    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write('')
            logger.info(f"created new file: {file_path}")

    try:
        with open(file_path, 'r') as f:
            content = f.read()
            logger.info(f"reading last order datetime from file: {content}")
        return content
    except:
        return 0

@app.route('/', methods=('GET', 'POST'))
def import_page():
	if request.method == 'POST':
		cutoff_date = request.form['date']
		print(cutoff_date)
	return render_template('import.html', last_order=recallLastOrder())

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=3002)