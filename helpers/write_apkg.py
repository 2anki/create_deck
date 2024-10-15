import os
import sys
import re
import tempfile

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

    # Ensure deck_payloads is defined before using it
    if deck_payloads:
        sanitized_name = sanitize_filename(deck_payloads[0]["name"])
    else:
        sanitized_name = "default"

    max_name_length = 255 - len(first_deck_id) - len('.apkg') - 1
    truncated_name = sanitized_name[:max_name_length]

    # Use a temporary file to avoid file name too long errors
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        output_filename = f'{truncated_name}-{first_deck_id}.apkg'
        tmp_file.name = output_filename

        try:
            package.write_to_file(tmp_file.name)
        except OSError as e:
            if e.errno == 36:  # File name too long
                # Handle the error, e.g., shorten the filename or move to a different directory
                print("File name too long. Shortening filename.")
                tmp_file.name = f'{truncated_name[:max_name_length - 10]}-truncated-{first_deck_id}.apkg'
                package.write_to_file(tmp_file.name)
            else:
                raise e  # Re-raise other exceptions

    final_path = os.path.join(os.getcwd() , tmp_file.name)
    os.rename(tmp_file.name, final_path)

    sys.stdout.write(final_path)