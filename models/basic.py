import json
import os

from genanki import Model

from fs_util import _read_template, get_template_path

DEFAULT_BASIC = json.loads(_read_template(get_template_path(), "n2a-basic.json", "", ""))


def basic_model(id, name, css, qfmt, afmt):
    if qfmt is None:
        qfmt = DEFAULT_BASIC.get('front')
    if afmt is None:
        afmt = DEFAULT_BASIC.get('back')

    return Model(id, name,
                 fields=DEFAULT_BASIC.get("fields"),
                 templates=[
                     {
                         "name": name,
                         "qfmt": qfmt,
                         "afmt": afmt,
                     }
                 ],
                 css=css,
                 )
