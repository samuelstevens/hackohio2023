from flask import Markup, render_template


def embed_greentext(raw: str) -> Markup:
    return Markup(render_template("greentext.html", post={"lines": raw.split("\n")}))


embed_table = {"greentext": embed_greentext}
