import dataclasses


from tttutor import html

from flask import Markup


@dataclasses.dataclass(frozen=True)
class Post:
    raw: str
    type: str
    topic: str
    facts: list[str]
    likes: int = 0

    def markup(self) -> Markup:
        if self.type == "greentext":
            return html.embed_greentext(self.raw)
        else:
            raise NotImplementedError(self.type)
