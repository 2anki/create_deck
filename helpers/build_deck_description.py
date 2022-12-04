"""
Helper function to add image to the deck description.
"""
from .read_template import _read_template


def _build_deck_description(template_dir, image):
    return _read_template(template_dir, "deck_description.html", "%s", image)
