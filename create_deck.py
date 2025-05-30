"""
This file is a modification on one of the test files of genanki[0].
It's used to create the APKG file from the JSON structure produced
by the Notion to Anki parser.

[0]: https://github.com/kerrickstaley/genanki
"""

import traceback
import json
import sys
import os

from genanki import Note
from genanki.util import guid_for

from helpers.cards import get_safe_value
from helpers.get_model import get_model
from helpers.get_model_id import get_model_id
from helpers.read_template import read_template
from helpers.sanitize_tags import sanitize_tags
from helpers.write_apkg import _write_new_apkg
from backend.utils.email_error_alert import send_error_email

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            raise IOError(
                'missing payload arguments(data file, deck style, template dir)')
        DATA_FILE = sys.argv[1]
        TEMPLATE_DIR = sys.argv[2]

        CLOZE_STYLE = read_template(TEMPLATE_DIR, "cloze_style.css", "", "")

        with open(DATA_FILE, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            media_files = []
            decks = []

            if len(data) == 0:
                sys.exit(1)

            # Model / Template stuff
            mt = data[0].get("settings", {})

            STYLING = data[0].get('style', "") or ""

            # Retreive template names for user or get the default ones
            cloze_model_name = mt.get('clozeModelName', "n2a-cloze") or "n2a-cloze"
            basic_model_name = mt.get('basicModelName', "n2a-basic") or "n2a-basic"
            input_model_name = mt.get('inputModelName', "n2a-input") or "n2a-input"

            # Set the model ids based on the template name
            input_model_id = mt.get('inputModelId', get_model_id(input_model_name))
            cloze_model_id = mt.get('clozeModelId', get_model_id(cloze_model_name))
            basic_model_id = mt.get('basicModelId', get_model_id(basic_model_name))
            template = mt.get('template', 'specialstyle')

            FMT_CLOZE_QUESTION = FMT_CLOZE_ANSWER = None
            FMT_INPUT_QUESTION = FMT_INPUT_ANSWER = None
            FMT_QUESTION = FMT_ANSWER = None

            # Respect user's choice of template
            if template == 'specialstyle':
                STYLING += read_template(TEMPLATE_DIR, "custom.css", "", "")
            elif template == 'nostyle':
                STYLING = ""
            elif template == 'abhiyan':
                STYLING = read_template(TEMPLATE_DIR, 'abhiyan.css', "", "")
                CLOZE_STYLE = read_template(TEMPLATE_DIR,
                                            "abhiyan_cloze_style.css", "", "")
                FMT_CLOZE_QUESTION = read_template(TEMPLATE_DIR,
                                                   "abhiyan_cloze_front.html",
                                                   "", "")
                FMT_CLOZE_ANSWER = read_template(TEMPLATE_DIR,
                                                 "abhiyan_cloze_back.html",
                                                 "", "")
                FMT_QUESTION = read_template(TEMPLATE_DIR,
                                             "abhiyan_basic_front.html", "",
                                             "")
                FMT_ANSWER = read_template(TEMPLATE_DIR, "abhiyan_basic_back.html",
                                           "",
                                           "")
                FMT_INPUT_QUESTION = read_template(TEMPLATE_DIR,
                                                   "abhiyan_input_front.html",
                                                   "", "")
                # Note: reusing the basic back, essentially the same.
                FMT_INPUT_ANSWER = read_template(TEMPLATE_DIR,
                                                 "abhiyan_basic_back.html",
                                                 "",
                                                 "")
            elif template == 'alex_deluxe':
                STYLING = read_template(TEMPLATE_DIR, 'alex_deluxe.css', "", "")
                CLOZE_STYLE = read_template(TEMPLATE_DIR,
                                            "alex_deluxe_cloze_style.css", "", "")
                FMT_CLOZE_QUESTION = read_template(TEMPLATE_DIR,
                                                   "alex_deluxe_cloze_front.html",
                                                   "", "")
                FMT_CLOZE_ANSWER = read_template(TEMPLATE_DIR,
                                                 "alex_deluxe_cloze_back.html", "",
                                                 "")
                FMT_QUESTION = read_template(TEMPLATE_DIR,
                                             "alex_deluxe_basic_front.html",
                                             "", "")
                FMT_ANSWER = read_template(TEMPLATE_DIR,
                                           "alex_deluxe_basic_back.html",
                                           "", "")
                FMT_INPUT_QUESTION = read_template(TEMPLATE_DIR,
                                                   "alex_deluxe_input_front.html",
                                                   "", "")
                FMT_INPUT_ANSWER = read_template(TEMPLATE_DIR,
                                                 "alex_deluxe_input_back.html", "",
                                                 "")
            # else notionstyle
            USE_CUSTOM_TEMPLATE = template == 'custom'
            CLOZE_STYLE = CLOZE_STYLE + "\n" + STYLING
            BASIC_STYLE = STYLING
            BASIC_FRONT = FMT_QUESTION
            BASIC_BACK = FMT_ANSWER
            n2aBasic = mt.get("n2aBasic")
            if n2aBasic and USE_CUSTOM_TEMPLATE:
                BASIC_STYLE = n2aBasic["styling"]
                BASIC_FRONT = n2aBasic["front"]
                BASIC_BACK = n2aBasic["back"]

            CLOZE_FRONT = FMT_CLOZE_QUESTION
            CLOZE_BACK = FMT_CLOZE_ANSWER
            n2aCloze = mt.get("n2aCloze")
            if n2aCloze and USE_CUSTOM_TEMPLATE:
                CLOZE_STYLE = n2aCloze["styling"]
                CLOZE_FRONT = n2aCloze["front"]
                CLOZE_BACK = n2aCloze["back"]

            n2aInput = mt.get("n2aInput")
            INPUT_FRONT = FMT_INPUT_QUESTION
            INPUT_BACK = FMT_INPUT_ANSWER
            INPUT_STYLE = STYLING
            if n2aInput and USE_CUSTOM_TEMPLATE:
                INPUT_STYLE = n2aInput["styling"]
                INPUT_FRONT = n2aInput["front"]
                INPUT_BACK = n2aInput["back"]

            for deck in data:
                cards = deck.get("cards", [])
                notes = []
                for card in cards:
                    tags = sanitize_tags(card.get('tags', []))
                    front = card.get("name", "")
                    back = card.get("back", "")
                    fields = [front, back, ",".join(card["media"])]
                    model = get_model(("basic", basic_model_id, basic_model_name,
                                       BASIC_STYLE, BASIC_FRONT, BASIC_BACK))
                    if card.get('cloze', False) and "{{c" in front:
                        model = get_model(
                            ("cloze", cloze_model_id, cloze_model_name,
                             CLOZE_STYLE, CLOZE_FRONT, CLOZE_BACK))
                    elif card.get('enableInput', False) and card.get('answer',
                                                                     False):
                        model = get_model(
                            ("input", input_model_id, input_model_name,
                             INPUT_STYLE, INPUT_FRONT, INPUT_BACK))
                        fields = [
                            front.replace("{{type:Input}}", ""),
                            back,
                            card["answer"],
                            ",".join(card["media"]),
                        ]

                    # Handle surrogates in the front and back
                    fields[0] = get_safe_value(fields[0])
                    fields[1] = get_safe_value(fields[1])

                    # Cards marked with -1 number means they are breaking
                    # compatability, treat them differently by using their
                    # respective Notion Id.
                    if card["number"] == -1 and "notionId" in card:
                        card["number"] = card["notionId"]

                    if mt.get("useNotionId") and "notionId" in card:
                        GUID = guid_for(card["notionId"])
                        my_note = Note(model, fields=fields,
                                       sort_field=card["number"], tags=tags,
                                       guid=GUID)
                        notes.append(my_note)
                    else:
                        my_note = Note(model, fields=fields,
                                       sort_field=card["number"], tags=tags)
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

        _write_new_apkg(decks, media_files)
    except Exception as e:
        if os.getenv('NODE_ENV') != 'production':
            raise e
        error_details = f"""
Error: {str(e)}
Traceback:
{traceback.format_exc()}
Environment:
DATA_FILE: {DATA_FILE if 'DATA_FILE' in locals() else 'N/A'}
TEMPLATE_DIR: {TEMPLATE_DIR if 'TEMPLATE_DIR' in locals() else 'N/A'}
"""
        send_error_email(f"[ERROR] [2anki.net] - {str(e)}", error_details)
        raise
