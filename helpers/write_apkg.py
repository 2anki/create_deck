import os
import sys
import re
from genanki import Deck, Package

"""
This module provides functionality to write a new Anki package file (.apkg) using provided deck payloads and media files.
"""

def sanitize_filename(filename):
    """
    Sanitize the filename by removing any character that is not alphanumeric, a space, or a hyphen.
    Replace spaces with hyphens.
    """
    sanitized = re.sub(
        r'[^\w\s\-\U0001F600-\U0001F64F]', '', filename, flags=re.UNICODE
    )
    sanitized = sanitized.replace(' ', '-')
    return sanitized

def _write_new_apkg(deck_payloads, media_files):
    """
    Write a new Anki package file (.apkg) using the provided deck payloads and media files.
    The filename is sanitized and truncated to ensure it is a safe Linux filename and does not exceed 255 characters.
    """
    first_deck_id = ""
    decks = []

    for deck_payload in deck_payloads:
        deck = Deck(
            deck_id=deck_payload["id"],
            name=deck_payload["name"],
            description=deck_payload["desc"]
        )

        if not first_deck_id:
            first_deck_id = str(deck_payload["id"])  # Convert to string

        for note in deck_payload["notes"]:
            deck.add_note(note)

        decks.append(deck)

    package = Package(decks)
    package.media_files = media_files

    # Ensure deck_payload is defined before using it
    if deck_payloads:
        sanitized_name = sanitize_filename(deck_payloads[0]["name"])
    else:
        sanitized_name = "default"

    max_name_length = 255 - len(first_deck_id) - len('.apkg') - 1
    truncated_name = sanitized_name[:max_name_length]

    output_filename = f'{truncated_name}-{first_deck_id}.apkg'

    package.write_to_file(output_filename)

    sys.stdout.write(os.getcwd() + "/" + output_filename)
