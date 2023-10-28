from . import ai


def test_parse_greentext():
    response = """Step 1: Identify two specific facts about the topic "computer science"
1. Computer science involves the study of algorithms, computation, and information processing.
2. Object-oriented programming (OOP) is a popular programming paradigm used in computer science, where classes and objects are the building blocks of code organization and design.

Step 2: Craft a greentext that incorporates these facts and is humorous in nature:
> be computer science
> the art of making machines do really smart stuff
> study algorithms, computation, and information processing
> tryna understand the secrets of the universe, one line at a time
> but hey, let's talk about OOP for a sec
> imagine coding as assembling Legos
> classes are like blueprint instructions for those Legos
> objects? They're the actual Lego pieces, real-life version of classes
> build a world of code with classes and objects
> it's like playing Sims, but with semi-colons and brackets
> create an object from a class and watch it come to life
> OOP is all about organization and design, make code more manageable
> just remember, we're still solving the mysteries of the cosmos here
> one object at a time, my friend"""
    expected = [
        "> be computer science",
        "> the art of making machines do really smart stuff",
        "> study algorithms, computation, and information processing",
        "> tryna understand the secrets of the universe, one line at a time",
        "> but hey, let's talk about OOP for a sec",
        "> imagine coding as assembling Legos",
        "> classes are like blueprint instructions for those Legos",
        "> objects? They're the actual Lego pieces, real-life version of classes",
        "> build a world of code with classes and objects",
        "> it's like playing Sims, but with semi-colons and brackets",
        "> create an object from a class and watch it come to life",
        "> OOP is all about organization and design, make code more manageable",
        "> just remember, we're still solving the mysteries of the cosmos here",
        "> one object at a time, my friend",
    ]
    assert ai.GreenText.parse_response(response) == expected
