"""
This file is a modifcation on one of the test files of genanki[0].
It's used to create the APKG file from the JSON structure produced
by the Notion to Anki parser.

[0]: https://github.com/kerrickstaley/genanki
"""

import hashlib
import json
import sys

import sentry_sdk
from genanki import Note
from genanki.util import guid_for

from helpers.get_model import get_model
from helpers.read_template import _read_template
from helpers.write_apkg import _wr_apkg

sentry_sdk.init(
    dsn="https://72be99d0475a4bfa9b0f24631571c96a@o1284472.ingest.sentry.io/6495216",
    traces_sample_rate=1.0
)


def model_id(name):
    """
    Preserve the old ids for backwards compatibility.
    :param name:
    :return:
    """
    if name == "n2a-input":
        return 6394002335189144856
    if name == "n2a-cloze":
        return 998877661
    if name == "n2a-basic":
        return 2020
    # https://stackoverflow.com/questions/16008670/how-to-hash-a-string-into-8-digits
    return abs(
        int(hashlib.sha1(name.encode("utf-8")).hexdigest(), 16) % (10 ** 8))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise IOError(
            'missing payload arguments(data file, deck style, template dir)')
    data_file = sys.argv[1]
    template_dir = sys.argv[2]

    CLOZE_STYLE = _read_template(template_dir, "cloze_style.css", "", "")

    with open(data_file, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        media_files = []
        decks = []

        # Model / Template stuff
        mt = data[0]["settings"]
        STYLING = data[0].get('style', "") or ""

        # Retreive template names for user or get the default ones
        cloze_model_name = mt.get('clozeModelName', "n2a-cloze") or "n2a-cloze"
        basic_model_name = mt.get('basicModelName', "n2a-basic") or "n2a-basic"
        input_model_name = mt.get('inputModelName', "n2a-input") or "n2a-input"

        # Set the model ids based on the template name
        input_model_id = mt.get('inputModelId', model_id(input_model_name))
        cloze_model_id = mt.get('clozeModelId', model_id(cloze_model_name))
        basic_model_id = mt.get('basicModelId', model_id(basic_model_name))
        template = mt.get('template', 'specialstyle')

        FMT_CLOZE_QUESTION = FMT_CLOZE_ANSWER = None
        FMT_INPUT_QUESTION = FMT_INPUT_ANSWER = None
        FMT_QUESTION = FMT_ANSWER = None

        # Respect user's choice of template
        if template == 'specialstyle':
            STYLING += _read_template(template_dir, "custom.css", "", "")
        elif template == 'nostyle':
            STYLING = ""
        elif template == 'abhiyan':
            STYLING = _read_template(template_dir, 'abhiyan.css', "", "")
            CLOZE_STYLE = _read_template(template_dir,
                                         "abhiyan_cloze_style.css", "", "")
            FMT_CLOZE_QUESTION = _read_template(template_dir,
                                                "abhiyan_cloze_front.html",
                                                "", "")
            FMT_CLOZE_ANSWER = _read_template(template_dir,
                                              "abhiyan_cloze_back.html",
                                              "", "")
            FMT_QUESTION = _read_template(template_dir,
                                          "abhiyan_basic_front.html", "",
                                          "")
            FMT_ANSWER = _read_template(template_dir, "abhiyan_basic_back.html",
                                        "",
                                        "")
            FMT_INPUT_QUESTION = _read_template(template_dir,
                                                "abhiyan_input_front.html",
                                                "", "")
            # Note: reusing the basic back, essentially the same.
            FMT_INPUT_ANSWER = _read_template(template_dir,
                                              "abhiyan_basic_back.html",
                                              "",
                                              "")
        elif template == 'alex_deluxe':
            STYLING = _read_template(template_dir, 'alex_deluxe.css', "", "")
            CLOZE_STYLE = _read_template(template_dir,
                                         "alex_deluxe_cloze_style.css", "", "")
            FMT_CLOZE_QUESTION = _read_template(template_dir,
                                                "alex_deluxe_cloze_front.html",
                                                "", "")
            FMT_CLOZE_ANSWER = _read_template(template_dir,
                                              "alex_deluxe_cloze_back.html", "",
                                              "")
            FMT_QUESTION = _read_template(template_dir,
                                          "alex_deluxe_basic_front.html",
                                          "", "")
            FMT_ANSWER = _read_template(template_dir,
                                        "alex_deluxe_basic_back.html",
                                        "", "")
            FMT_INPUT_QUESTION = _read_template(template_dir,
                                                "alex_deluxe_input_front.html",
                                                "", "")
            FMT_INPUT_ANSWER = _read_template(template_dir,
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
                fields = [card["name"], card["back"], ",".join(card["media"])]
                model = get_model(("basic", basic_model_id, basic_model_name,
                                   BASIC_STYLE, BASIC_FRONT, BASIC_BACK))
                if card.get('cloze', False) and "{{c" in card["name"]:
                    model = get_model(
                        ("cloze", cloze_model_id, cloze_model_name,
                         CLOZE_STYLE, CLOZE_FRONT, CLOZE_BACK))
                elif card.get('enableInput', False) and card.get('answer',
                                                                 False):
                    model = get_model(
                        ("input", input_model_id, input_model_name,
                         INPUT_STYLE, INPUT_FRONT, INPUT_BACK))
                    fields = [
                        card["name"].replace("{{type:Input}}", ""),
                        card["back"],
                        card["answer"],
                        ",".join(card["media"]),
                    ]
                # Cards marked with -1 number means they are breaking
                # compatability, treat them differently by using their
                # respective Notion Id.
                if card["number"] == -1 and "notionId" in card:
                    card["number"] = card["notionId"]

                if mt.get("useNotionId") and "notionId" in card:
                    GUID = guid_for(card["notionId"])
                    my_note = Note(model, fields=fields,
                                   sort_field=card["number"], tags=card['tags'],
                                   guid=GUID)
                    notes.append(my_note)
                else:
                    my_note = Note(model, fields=fields,
                                   sort_field=card["number"], tags=card['tags'])
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
