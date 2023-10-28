"""
Does all the AI-related stuff.
"""

import os
import openai


from flask import Markup, render_template

openai.api_key = os.getenv("OPENAI_API_KEY")


def load_prompt(filename):
    with open(os.path.join("prompts", filename)) as fd:
        return fd.read().strip() + "\n"


# Constants
system_prompt = load_prompt("system.txt")
greentext_prompt = load_prompt("greentext.txt")


class ShortFormContent:
    def new(self, *, topic=None, facts=None, n=10):
        raw = self.get_raw_content(topic=topic, facts=facts, n=n)
        embedded = self.embed_in_html(raw)
        return embedded

    def get_raw_content(self, *, topic=None, facts=None, n=10):
        """Gets raw content, like a greentext or a tweet, using a template and a request to OpenAI's servers."""
        raise NotImplementedError()

    def embed_in_html(self, raw):
        """Embeds raw content in html.

        raw: (list[str]) list of raw content, in content-specific format.
        """
        raise NotImplementedError()


class GreenText(ShortFormContent):
    def get_raw_content(self, *, topic=None, facts=None, n=10):
        if not topic and not facts:
            raise ValueError("Missing topic and facts")

        user_prompt = greentext_prompt
        if topic:
            user_prompt += f"\nCan you make a greentext about the topic:\n\n{topic}\n"

        if facts:
            assert isinstance(facts, list), type(facts)

            user_prompt += "\nThe facts are:\n"
            for i, fact in enumerate(facts):
                user_prompt += f"\n {i + 1}. {fact}\n"

        else:
            user_prompt += "\nThink step by step, first writing the two specific facts, then writing the greentext in a way that naturally incorporates those facts."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            n=n,
        )

        raw = []

        # Need to parse the response
        for choice in response.choices:
            raw.append(self.parse_response(choice.message.content))

        return raw

    def embed_in_html(self, raw):
        return [
            Markup(render_template("greentext.html", post={"lines": lines}))
            for lines in raw
        ]

    @staticmethod
    def parse_response(response):
        return [line.strip() for line in response.split("\n") if line.startswith(">")]


class DummyGreenText:
    def html(self):
        return Markup(render_template("dummy-greentext.html"))
