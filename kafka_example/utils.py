import uuid
import random


def create_data_identifier(obj=None):
    """
    Generate a data identifier for something.
    """
    # Hardcoded to this app
    # example:[uid]
    return "example:%s" % str(uuid.uuid1())


def random_message():
    """
    Return some random message
    """
    PEOPLE = [
        "Homer", "Marge", "Bart", "Lisa", "Maggie", "Moe", "Barney", 
        "Carl", "Lenny", "Mr. Burns", "McBain", 
        "Krusty the Klown", "Sideshow Mel", "Sideshow Bob",
        "Milhouse", "Nelson", "Ned Flanders", 
        "Professor Frink", "Kent Brockman",
    ]
    PLACES = [
        "642 Evergreen Terrace", "Moe's Bar", "Springfield Elementary",
        "Springfield Nuclear Power Plant", "Capital City",
    ]
    return "%s calls %s from %s" % (
        random.choice(PEOPLE),
        random.choice(PEOPLE),
        random.choice(PLACES),
    )
