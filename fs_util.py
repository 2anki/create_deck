"""
utility functions
"""
import os
import sys

from genanki import Deck
from genanki import Package


def _wr_apkg(payload, media_files):
    first_id = ""
    decks = []

    for deck_payload in payload:
        deck = Deck(deck_id=deck_payload["id"], name=deck_payload["name"],
                    description=deck_payload["desc"])
        if not first_id:
            first_id = deck_payload["id"]
        for note in deck_payload["notes"]:
            deck.add_note(note)
        decks.append(deck)

    pkg = Package(decks)
    pkg.media_files = media_files
    fout_anki = "{NAME}.apkg".format(NAME=first_id)

    pkg.write_to_file(fout_anki)
    sys.stdout.write(os.getcwd() + "/" + fout_anki)


def _path_start():
    if sys.platform == "win32":
        return "C:"
    return "/"


def get_template_path():
    """
    helper to find path to the server's template directory
    :return:
    """
    return os.path.dirname(__file__) + "/../server/src/templates/"


def _read_template(template_dir, path, fmt, value):
    file_path = path if path.startswith(_path_start()) else template_dir + path
    with open(file_path, "r", encoding="utf-8") as file:
        if fmt and value:
            return file.read().replace(fmt, value)
        return file.read()


def _build_deck_description(template_dir, image):
    return _read_template(template_dir, "deck_description.html", "%s", image)
