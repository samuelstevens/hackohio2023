"""
Does all the AI-related stuff.
"""

import os
import json
import openai

from tttutor import schema

openai.api_key = "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"


def load_prompt(filename):
    with open(os.path.join("prompts", filename)) as fd:
        return fd.read().strip() + "\n"


# Constants
system_prompt = load_prompt("system.txt")
greentext_prompt = load_prompt("greentext.txt")
reddit_prompt = load_prompt("reddit.txt")
tweet_prompt = load_prompt("tweets.txt")


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
    return posts


def get_reddit_posts(*, topic=None, facts=None, n=10) -> list[schema.Post]:
    if not topic and not facts:
        raise ValueError("Missing topic and facts")

    if facts is None:
        facts = []

    prefix = "Reddit Post:"
    user_prompt = reddit_prompt.format(topic=topic, prefix=prefix)

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
        text = "".join(
            line.lstrip(">").strip()
            for line in choice.message.content.split("\n")
            if line.startswith(">")
        )
        raw = json.dumps({"text": text, "title": topic.capitalize()})
        post = schema.Post(raw, "reddit", topic, facts)
        posts.append(post)
    return posts


def get_tweets(*, topic=None, facts=None, n=10) -> list[schema.Post]:
    if not topic and not facts:
        raise ValueError("Missing topic and facts")

    if facts is None:
        facts = []

    user_prompt = tweet_prompt
    user_prompt += f"\nNow please make a tweet about the topic:\n\n{topic}\n"
    user_prompt += "\nThink step by step and explain the joke before writing the tweet. Be sure to format your tweet with '> ' as a prefix."

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
        raw = "".join(
            line.lstrip(">").strip()
            for line in choice.message.content.split("\n")
            if line.startswith(">")
        )
        post = schema.Post(raw, "tweet", topic, facts)
        posts.append(post)
    return posts
