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
    Replace spaces with hyphens. Ensures the result is safe for use as a filename.
    """
    # Remove path separators and other dangerous characters
    sanitized = re.sub(
        r'[^\w\s\-\U0001F600-\U0001F64F]', '', filename, flags=re.UNICODE
    )
    sanitized = sanitized.replace(' ', '-')
    # Use basename to ensure no directory traversal is possible
    return os.path.basename(sanitized)

def create_decks(deck_payloads):
    """
    Create decks from the provided deck payloads.

    Args:
        deck_payloads (list): List of dictionaries containing deck information.

    Returns:
        tuple: A tuple containing the list of created decks and the ID of the first deck.
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
            first_deck_id = str(deck_payload["id"])

        for note in deck_payload["notes"]:
            deck.add_note(note)

        decks.append(deck)

    return decks, first_deck_id

def write_package_to_temp_file(package):
    """
    Write the package to a temporary file.

    Args:
        package (Package): The package to be written to a file.

    Returns:
        str: The path to the temporary file.
    """
    temp_filename = f"temp_apkg_{uuid.uuid4().hex}.apkg"
    temp_path = os.path.join(tempfile.gettempdir(), temp_filename)

    try:
        package.write_to_file(temp_path)
    except Exception as e:
        print(f"Error writing to temporary file: {e}")
        raise

    return temp_path

def rename_temp_file(temp_path, sanitized_name, first_deck_id):
    """
    Rename the temporary file to a final filename.

    Args:
        temp_path (str): The path to the temporary file.
        sanitized_name (str): The sanitized name for the final file.
        first_deck_id (str): The ID of the first deck.

    Returns:
        str: The path to the final file.
    """
    # Check for path traversal attempts in the original inputs
    name_str = str(sanitized_name)
    id_str = str(first_deck_id)
    
    # Detect dangerous path components before sanitization
    dangerous_patterns = ['..', '/', '\\', ':']
    for pattern in dangerous_patterns:
        if pattern in name_str or pattern in id_str:
            raise ValueError("Path traversal attempt detected in filename")
    
    # Now safely extract just the filename components
    safe_name = os.path.basename(name_str)
    safe_deck_id = os.path.basename(id_str)
    
    base_filename = f'{safe_name}-{safe_deck_id}'
    max_filename_length = 255

    if len(base_filename) + len(".apkg") > max_filename_length:
        base_filename = base_filename[:max_filename_length - len(".apkg") - 10] + "-trunc"

    final_filename = f"{base_filename}.apkg"
    # Ensure the filename contains no path separators (double-check)
    final_filename = os.path.basename(final_filename)
    
    # Construct the final path safely within the current working directory
    cwd = os.getcwd()
    final_path = os.path.join(cwd, final_filename)
    
    # Verify that the resolved path is still within the current working directory
    real_final_path = os.path.realpath(final_path)
    real_cwd = os.path.realpath(cwd)
    
    if not real_final_path.startswith(real_cwd + os.sep) and not real_final_path == real_cwd:
        raise ValueError("Path traversal attempt detected in final path")

    try:
        os.rename(temp_path, final_path)
    except OSError as e:
        if e.errno == 36:
            short_final_filename = f"deck_{uuid.uuid4().hex[:8]}.apkg"
            # Apply the same safety checks to the fallback filename
            short_final_filename = os.path.basename(short_final_filename)
            final_path = os.path.join(cwd, short_final_filename)
            
            # Verify the fallback path is safe too
            real_final_path = os.path.realpath(final_path)
            if not real_final_path.startswith(real_cwd + os.sep) and not real_final_path == real_cwd:
                raise ValueError("Path traversal attempt detected in fallback filename")
                
            os.rename(temp_path, final_path)
            print(f"Warning: Filename too long. Saved as {final_path}")
        else:
            print(f"Error renaming file: {e}")
            raise

    return final_path

def _write_new_apkg(deck_payloads, media_files):
    """
    Write a new Anki package file (.apkg) using provided deck payloads and media files.

    Args:
        deck_payloads (list): List of dictionaries containing deck information.
        media_files (list): List of media files to be included in the package.
    """
    decks, first_deck_id = create_decks(deck_payloads)
    package = Package(decks)
    package.media_files = media_files

    sanitized_name = sanitize_filename(deck_payloads[0]["name"]) if deck_payloads else "default"
    temp_path = write_package_to_temp_file(package)
    final_path = rename_temp_file(temp_path, sanitized_name, first_deck_id)

    # Handle Unicode characters properly for Windows console
    try:
        sys.stdout.write(final_path)
    except UnicodeEncodeError:
        # If Unicode encoding fails, encode to bytes and write to stdout buffer
        sys.stdout.buffer.write(final_path.encode('utf-8'))
