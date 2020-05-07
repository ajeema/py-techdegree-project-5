# Credit:
# https://charlesleifer.com/blog/how-to-make-a-flask-blog-in-one-hour-or-less/

from flask import Flask, g, render_template, flash, redirect, url_for, abort
from flask_bcrypt import check_password_hash
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)


import forms
import models


DEBUG = True
PORT = 8000
HOST = "0.0.0.0"

app = Flask(__name__)
app.secret_key = "auoesh.bouoastuh.43,uoausoehuosth3ououea.auoub!"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.route("/login", methods=("GET", "POST"))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for("index"))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template("account/login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for("index"))


@app.route("/")
def index():
    stream = models.Entry.select().limit(4)
    return render_template("index.html", stream=stream)


@app.route("/entries")
def entries():
    stream = models.Entry.select()
    return render_template("entries/all_entries.html", stream=stream)


@app.route("/new_entry", methods=("GET", "POST"))
@login_required
def entry():
    form = forms.EntryForm()
    if form.validate_on_submit():
        entry_new = models.Entry.create(
            user=g.user.id,
            content=form.content.data.strip(),
            title=form.title.data,
            time_spent=form.time_spent.data,
            resources=form.resources.data,
        )
        entry_new.create_and_add_tags(form.tags.data)
        flash("Journal Entry done!", "success")
        return redirect(url_for("index"))
    return render_template("entries/new.html", form=form)


@app.route("/entries/edit/<slug>", methods=("GET", "POST"))
@login_required
def edit(slug):
    entry = models.Entry.select().where(models.Entry.slug == slug).get()
    form = forms.EditEntryForm(obj=entry)
    if form.validate_on_submit():
        entry.title = form.title.data
        entry.time_spent = form.time_spent.data
        entry.content = form.content.data
        entry.resources = form.resources.data
        entry.tags.clear()
        for tag in form.tags.data:
            if tag not in [tag for tag in entry.tags]:
                try:
                    tag.save(force_insert=True)
                except models.IntegrityError:
                    pass  # Tag already exists do not need to create
                entry.tags.add([tag])
        entry.save()
        flash("Entry edited.", "success")
        return redirect(url_for("index"))
    return render_template("entries/edit.html", form=form, entry=entry)


@app.route("/entries/delete/<slug>")
def delete(slug=None):
    models.Entry.get(models.Entry.slug == slug).delete_instance()
    flash("Deleted!", "success")
    return redirect(url_for("index"))


@app.route("/entry/<slug>")
def view_entry(slug=None):
    entry = models.Entry.select().where(models.Entry.slug == slug)
    if entry.count() == 0:
        abort(404)
    return render_template("entries/detail.html", stream=entry)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.route("/entries/tags/{{tag}}")
def tag(tag=None):
    tag = models.Entry.select().where(models.Entry.tag == tag)
    return render_template("tags_list.html")


@app.route("/tags/<slug>")
@login_required
def tag_entries(slug):
    """List entries that include a single tag"""
    tag = models.Tag.get(models.Tag.slug == slug)
    return render_template("entries/tags_list.html", tag=tag, entry=tag.entry)


if __name__ == "__main__":
    models.initialize()
    try:
        models.User.create_user(
            username="bossman",
            email="user@email.com",
            password="password",
            admin=True,
        )
    except ValueError:
        pass
    app.jinja_env.cache = {}
    app.run(debug=DEBUG, host=HOST, port=PORT)
