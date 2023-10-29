import sqlite3
import json

import click
from flask import current_app, g

from tttutor import schema


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def save_posts(posts: list[schema.Post]):
    db = get_db()
    values = [(post.raw, post.type, post.topic, ",".join(post.facts)) for post in posts]
    try:
        db.executemany(
            "INSERT INTO post (raw, type, topic, facts, likes) VALUES (?, ?, ?, ?, 0)",
            values,
        )
        db.commit()
    except sqlite3.IntegrityError:
        pass


def load_posts(*, topic: str, n: int) -> list[schema.Post]:
    db = get_db()
    stmt = "SELECT raw, type, topic, facts FROM post WHERE topic LIKE ? LIMIT (?)"
    return [
        schema.Post(raw, type, topic, facts.split(","))
        for raw, type, topic, facts in db.execute(stmt, (f"%{topic}%", n)).fetchall()
    ]


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

    with current_app.open_resource("examples.json") as fd:
        posts = [schema.Post(**row) for row in json.load(fd)]
    save_posts(posts)


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
