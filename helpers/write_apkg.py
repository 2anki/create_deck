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

def _write_new_apkg(deck_payloads, media_files):
    """
    Write a new Anki package file (.apkg) using the provided deck payloads and media files.
    The filename is sanitized and a unique identifier is used to avoid filename length issues.
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

    if deck_payloads:
        sanitized_name = sanitize_filename(deck_payloads[0]["name"])
    else:
        sanitized_name = "default"

    # Create a unique filename for the temporary file
    temp_filename = f"temp_apkg_{uuid.uuid4().hex}.apkg"
    temp_path = os.path.join(tempfile.gettempdir(), temp_filename)

    try:
        package.write_to_file(temp_path)
    except Exception as e:
        print(f"Error writing to temporary file: {e}")
        raise

    # Create the final filename, truncate if necessary
    base_filename = f'{sanitized_name}-{first_deck_id}'
    max_filename_length = 255  # Maximum filename length for most systems
    if len(base_filename) + len(".apkg") > max_filename_length:
        base_filename = base_filename[:max_filename_length - len(".apkg") - 10] + "-trunc"

    final_filename = f"{base_filename}.apkg"
    final_path = os.path.join(os.getcwd(), final_filename)

    try:
        os.rename(temp_path, final_path)
    except OSError as e:
        # Handle potential long filename issues on final rename
        if e.errno == 36:  # OSError: [Errno 36] File name too long
            short_final_filename = f"deck_{uuid.uuid4().hex[:8]}.apkg"
            final_path = os.path.join(os.getcwd(), short_final_filename)
            os.rename(temp_path, final_path)
            print(f"Warning: Filename too long. Saved as {final_path}")
        else:
            print(f"Error renaming file: {e}")
            raise

    sys.stdout.write(final_path)
