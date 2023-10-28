import os

from flask import Flask, request, render_template

from . import ai


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

    @app.route("/ping")
    def ping():
        return "ping"

    @app.route("/search")
    def search():
        return render_template("search.html")

    @app.route("/posts", methods=("GET", "POST"))
    def posts():
        facts = []

        if request.method == "POST":
            # Get the content
            topic = request.form.get("topic")
            dev_mode = request.form.get("dev", "prod")
        elif request.method == "GET":
            topic = request.args.get("topic")
            dev_mode = request.args.get("dev", "prod")

        if not topic and not facts:
            posts = []
            title = "Search"
        else:
            if dev_mode == "cache-only":
                # Load from cache
                raise NotImplementedError()
            elif dev_mode == "no-cache":
                shortform = ai.GreenText()
                posts = shortform.new(topic=topic, n=1)
            elif dev_mode == "prod":
                raise NotImplementedError()
            else:
                raise ValueError()
            title = topic
            print(posts)

        return render_template("posts.html", posts=posts, title=title)

    @app.route("/api/more")
    def more():
        breakpoint()

    return app
