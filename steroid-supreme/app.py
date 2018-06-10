#! /usr/bin/env python3
from flask import Flask, render_template, request
import subprocess


DEBUG = False

app = Flask(__name__)
app.secret_key = 'SUPERSECRETKEY'


@app.route('/index')
@app.route('/')
def index():
    args = {'active': 'index'}
    return render_template('index.html', args=args)


@app.route('/about')
def about():
    args = {'active': 'about'}
    return render_template('about.html', args=args)


@app.route('/filebrowser', methods=['GET', 'POST'])
def filebrowser():
    args = {'active': 'filebrowser', 'output': 'Enter a directory to see its contents'}
    if request.method == 'GET':
        return render_template('filebrowser.html', args=args)
    else:
        directory = request.form['directory']
        command = 'ls {}'.format(directory)
        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
        output = output.replace('\n', '<br>')
        args['output'] = output
        return render_template('filebrowser.html', args=args)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=DEBUG)
