import random

from flask import Blueprint, Markup, render_template, request

from tttutor import ai, db

bp = Blueprint("api", __name__, url_prefix="/api")


def dummy_reddit():
    return Markup(render_template("dummy-reddit.html"))


def dummy_twitter():
    return Markup(render_template("dummy-twitter.html"))


@bp.route("/more")
def more():
    """Get more posts, returned as html for htmx."""
    facts = []
    topic = request.args.get("topic")
    dev_mode = request.args.get("dev", "prod")

    n = 10

    if topic or facts:
        if dev_mode == "cache-only":
            # Load from cache
            posts = db.load_posts(topic=topic, n=n)

        elif dev_mode == "no-cache":
            posts = ai.get_greentexts(topic=topic, n=n)
            db.save_posts(posts)

        elif dev_mode == "prod":
            # Load half from cache, half from openai
            posts = db.load_posts(topic=topic, n=n // 2)

            n = n - len(posts)
            if n > 0:
                fn = random.choice(
                    [ai.get_greentexts, ai.get_reddit_posts, ai.get_tweets]
                )
                new_posts = fn(topic=topic, n=n)
                db.save_posts(new_posts)

                posts += new_posts

            random.shuffle(posts)
        else:
            raise ValueError(dev_mode)
        front_posts = posts[:3]
        back_posts = posts[3:]

        return (
            "\n".join(render_template("post.html", post=post) for post in front_posts)
            + render_template("on_reveal.html", topic=topic)
            + "\n".join(render_template("post.html", post=post) for post in back_posts)
            + """<div id="end">Out of posts!</div>"""
        )

    return ""


@bp.route("/like", methods=["POST"])
def like():
    """Increment post's likes in database."""
    breakpoint()
