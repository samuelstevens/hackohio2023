"""
Does all the AI-related stuff.
"""

import os
import openai

from tttutor import schema

openai.api_key = os.getenv("OPENAI_API_KEY")


def load_prompt(filename):
    with open(os.path.join("prompts", filename)) as fd:
        return fd.read().strip() + "\n"


# Constants
system_prompt = load_prompt("system.txt")
greentext_prompt = load_prompt("greentext.txt")


def get_greentexts(*, topic=None, facts=None, n=10) -> list[schema.Post]:
    """
    Returns n strings that represent 'raw' greentexts
    """
    if not topic and not facts:
        raise ValueError("Missing topic and facts")

    if facts is None:
        facts = []

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

    posts = []
    for choice in response.choices:
        raw = "\n".join(
            line.strip()
            for line in choice.message.content.split("\n")
            if line.startswith(">")
        )
        post = schema.Post(raw, "greentext", topic, facts)
        posts.append(post)


def dummy_reddit():
        return Markup(render_template("dummy-reddit.html"))
