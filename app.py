import os

from flask import Flask, render_template
app = Flask(__name__)


@app.route('/entries')
def entries():
    return render_template("index.html")

@app.route('/entries/new')
def new_entries():
    return render_template("new.html")

@app.route('/entries/<id>')
def entry_id():
    return "Entry ID"

@app.route('/entries/<id>/edit')
def entries_edit():
    return render_template("edit.html")

@app.route('/entries/<id>/delete')
def entry_delete():
    return "Delete an entry!"

@app.route('/')
def home():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)
