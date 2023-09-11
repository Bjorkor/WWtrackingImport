from flask import Flask, render_template, request, url_for, flash, redirect, session

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=3002)