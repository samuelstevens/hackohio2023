import os

from flask import Flask, render_template

from . import db, posts, api


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "tttutor.sqlite3"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    @app.route("/ping")
    def ping():
        return "ping"

    app.register_blueprint(posts.bp)
    app.register_blueprint(api.bp)

    @app.route("/")
    def home():
        return render_template("home.html", posts=[], title="")

    return app
