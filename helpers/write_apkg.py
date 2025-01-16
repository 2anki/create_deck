"""
This module provides functionality to write a new Anki package file (.apkg) using provided deck payloads and media files.
"""

import os
import sys
import re
import tempfile
import uuid

from genanki import Deck, Package

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

def create_decks(deck_payloads):
    first_deck_id = ""
    decks = []

    for deck_payload in deck_payloads:
        deck = Deck(
            deck_id=deck_payload["id"],
            name=deck_payload["name"],
            description=deck_payload["desc"]
        )

        if not first_deck_id:
            first_deck_id = str(deck_payload["id"])

        for note in deck_payload["notes"]:
            deck.add_note(note)

        decks.append(deck)

    return decks, first_deck_id

def write_package_to_temp_file(package):
    temp_filename = f"temp_apkg_{uuid.uuid4().hex}.apkg"
    temp_path = os.path.join(tempfile.gettempdir(), temp_filename)

    try:
        package.write_to_file(temp_path)
    except Exception as e:
        print(f"Error writing to temporary file: {e}")
        raise

    return temp_path

def rename_temp_file(temp_path, sanitized_name, first_deck_id):
    base_filename = f'{sanitized_name}-{first_deck_id}'
    max_filename_length = 255

    if len(base_filename) + len(".apkg") > max_filename_length:
        base_filename = base_filename[:max_filename_length - len(".apkg") - 10] + "-trunc"

    final_filename = f"{base_filename}.apkg"
    final_path = os.path.join(os.getcwd(), final_filename)

    try:
        os.rename(temp_path, final_path)
    except OSError as e:
        if e.errno == 36:
            short_final_filename = f"deck_{uuid.uuid4().hex[:8]}.apkg"
            final_path = os.path.join(os.getcwd(), short_final_filename)
            os.rename(temp_path, final_path)
            print(f"Warning: Filename too long. Saved as {final_path}")
        else:
            print(f"Error renaming file: {e}")
            raise

    return final_path

def _write_new_apkg(deck_payloads, media_files):
    decks, first_deck_id = create_decks(deck_payloads)
    package = Package(decks)
    package.media_files = media_files

    sanitized_name = sanitize_filename(deck_payloads[0]["name"]) if deck_payloads else "default"
    temp_path = write_package_to_temp_file(package)
    final_path = rename_temp_file(temp_path, sanitized_name, first_deck_id)

    sys.stdout.write(final_path)
