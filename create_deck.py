"""
This file is a modification on one of the test files of genanki[0].
It's used to create the APKG file from the JSON structure produced
by the Notion to Anki parser.

[0]: https://github.com/kerrickstaley/genanki
"""

import json
import sys

import sentry_sdk
from genanki import Note
from genanki.util import guid_for

from helpers.anki_template_file import AnkiTemplateFile
from helpers.get_model import get_model
from helpers.read_template import _read_template
from helpers.write_apkg import _wr_apkg

sentry_sdk.init(
    dsn="https://72be99d0475a4bfa9b0f24631571c96a@o1284472.ingest.sentry.io/6495216",
    traces_sample_rate=1.0
)


def create_deck(data_file, template_dir):
    """
    Create Anki deck in APKG format.
    """
    if data_file and template_dir:

        with open(data_file, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            media_files = []
            decks = []

            # Model / Template stuff
            deck_settings = data[0]["settings"]
            template_selection = deck_settings.get('template', 'specialstyle')

            # Retrieve template names for user or get the default ones
            cloze_template = AnkiTemplateFile(deck_settings, "cloze",
                                              template_dir, template_selection)
            input_template = AnkiTemplateFile(deck_settings, "input",
                                              template_dir, template_selection)
            basic_template = AnkiTemplateFile(deck_settings, "basic",
                                              template_dir, template_selection)

            cloze_template.style += "\n" + _read_template(template_dir,
                                                          "cloze_style.css", "",
                                                          "")

            # Respect user's choice of template
            if template_selection == 'nostyle':
                basic_template.clear_style()
                cloze_template.clear_style()
                input_template.clear_style()
            elif template_selection == 'abhiyan':
                cloze_template.load_user_file(template_dir, 'abhiyan')
                basic_template.load_user_file(template_dir, 'abhiyan')
                input_template.load_user_file(template_dir, 'abhiyan')
            elif template_selection == 'alex_deluxe':
                cloze_template.load_user_file(template_dir, 'alex_deluxe')
                basic_template.load_user_file(template_dir, 'alex_deluxe')
                input_template.load_user_file(template_dir, 'alex_deluxe')
            elif template_selection == 'custom':
                basic_template.override_values(deck_settings.get("n2aBasic"))
                cloze_template.override_values(deck_settings.get("n2aCloze"))
                input_template.override_values(deck_settings.get("n2aInput"))

            for deck in data:
                cards = deck.get("cards", [])
                notes = []
                for card in cards:
                    fields = [card["name"], card["back"],
                              ",".join(card["media"])]
                    model = get_model(
                        ("basic", basic_template.id, basic_template.name,
                         basic_template.style, basic_template.front,
                         basic_template.back))
                    if card.get('cloze', False) and "{{c" in card["name"]:
                        model = get_model(
                            ("cloze", cloze_template.id, cloze_template.name,
                             cloze_template.style, cloze_template.front,
                             cloze_template.back))
                    elif card.get('enableInput', False) and card.get('answer',
                                                                     False):
                        model = get_model(
                            ("input", input_template.id, input_template.name,
                             input_template.style, input_template.front,
                             input_template.back))
                        fields = [
                            card["name"].replace("{{type:Input}}", ""),
                            card["back"],
                            card["answer"],
                            ",".join(card["media"]),
                        ]
                    # Cards marked with -1 number means they are breaking
                    # compatibility, treat them differently by using their
                    # respective Notion id.
                    if card["number"] == -1 and "notionId" in card:
                        card["number"] = card["notionId"]

                    if deck_settings.get("useNotionId") and "notionId" in card:
                        guid = guid_for(card["notionId"])
                        my_note = Note(model, fields=fields,
                                       sort_field=card["number"],
                                       tags=card['tags'],
                                       guid=guid)
                        notes.append(my_note)
                    else:
                        my_note = Note(model, fields=fields,
                                       sort_field=card["number"],
                                       tags=card['tags'])
                        notes.append(my_note)
                    media_files = media_files + card["media"]
                decks.append(
                    {
                        "notes": notes,
                        "id": deck["id"],
                        "desc": "",
                        "name": deck["name"],
                    }
                )

        _wr_apkg(decks, media_files)
        return
    raise IOError(
        'missing payload arguments(data file, deck style, template dir)')


if __name__ == "__main__":
    create_deck(sys.argv[1], sys.argv[2])
