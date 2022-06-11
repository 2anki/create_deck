"""
Input note model
"""
import json

from genanki import Model

from fs_util import _read_template, get_template_path

DEFAULT_INPUT = json.loads(
    _read_template(get_template_path(), "n2a-input.json", "", "")
)


def input_model(model_id, name, css, qfmt, afmt):
    """
    The input note type
    :param model_id: model id
    :param name: note name
    :param css: note styling
    :param qfmt: note front markup
    :param afmt: note back markup
    :return: Note model
    """
    if qfmt is None:
        qfmt = DEFAULT_INPUT.get("front")
    if afmt is None:
        afmt = DEFAULT_INPUT.get("back")
    return Model(model_id, name,
                 fields=DEFAULT_INPUT.get("fields"),
                 templates=[
                     {
                         "name": name,
                         "qfmt": qfmt,
                         "afmt": afmt,
                     }
                 ],
                 css=css,
                 )
