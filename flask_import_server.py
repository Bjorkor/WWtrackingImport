from flask import Flask, render_template, request, url_for, flash, redirect, session
import os
import flask_import_module

app = Flask(__name__)


def recallLastOrder():
    file_path = '/home/ftp/WWtrackingImport/lastorder'

    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return content
    except:
        return 0


@app.route('/', methods=('GET', 'POST'))
def import_page():
    if request.method == 'POST':
        cutoff_date = request.form['date']
        print(cutoff_date)
        print(flask_import_module.main_work())
    return render_template('import.html', last_order=recallLastOrder())


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=3002)
