"""
Cloze deletion note model
"""
import json

from genanki import Model

from fs_util import _read_template, get_template_path

DEFAULT_CLOZE = json.loads(
    _read_template(get_template_path(), "n2a-cloze.json", "", ""))


def cloze_model(model_id, name, css, qfmt, afmt):
    """
    The basic note type
    :param model_id: model id
    :param name: note name
    :param css: note styling
    :param qfmt: note front markup
    :param afmt: note back markup
    :return: Note model
    """
    if qfmt is None:
        qfmt = DEFAULT_CLOZE.get('front')
    if afmt is None:
        afmt = DEFAULT_CLOZE.get('back')

    return Model(
        model_id, name,
        fields=DEFAULT_CLOZE.get("fields"),
        templates=[
            {
                "name": name,
                "qfmt": qfmt,
                "afmt": afmt,
            },
        ],
        css=css,
        model_type=Model.CLOZE,
    )
