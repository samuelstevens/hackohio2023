import json
import random
import os

from flask import render_template, Markup, current_app, url_for


def random_username() -> str:
    return random.choice(
        [
            "brutus",
            "kristina-johnson",
            "ticketbay-dev",
            "marvin-harrison-jr",
            "XichiganSucks23",
        ]
    )


def random_name() -> str:
    return random.choice(
        [
            "Brutus",
            "Kristina",
            "Sam",
            "Blake",
            "Xander",
            "Kanye",
            "ElonMusk",
        ]
    )


def random_time():
    hours = random.choice(range(23))
    return f"{hours}hr ago"


def random_img():
    meme_dir = os.path.join(current_app.root_path, "static/images/memes")
    choices = os.listdir(meme_dir)
    choice = random.choice(choices)

    return url_for("static", filename=f"images/memes/{choice}")


def random_video():
    meme_dir = os.path.join(current_app.root_path, "static/videos")
    choices = list(set(os.path.splitext(path)[0] for path in os.listdir(meme_dir)))
    choice = random.choice(choices)

    return url_for("static", filename=f"videos/{choice}")


def embed_greentext(raw: str) -> Markup:
    post = {"lines": raw.split("\n"), "img": random_img()}
    return Markup(render_template("greentext.html", post=post))


def embed_reddit(raw: str) -> Markup:
    post = json.loads(raw)
    post["author"] = random_username()
    post["time"] = random_time()
    post["img"] = random_img()
    post["upvotes"] = random.randint(-10, 5000)
    return Markup(render_template("reddit.html", post=post))


def embed_tweet(raw: str) -> Markup:
    post = {
        "text": raw,
        "username": random_username(),
        "author": random_name(),
        "likes": f"{random.randint(3, 900)}.{random.randint(0, 9)}K",
        "replies": random.randint(10, 100),
        "img": random_img(),
    }

    return Markup(render_template("twitter.html", post=post))
