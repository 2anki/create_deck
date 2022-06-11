"""
Basic note model
"""
import json

from genanki import Model

from fs_util import _read_template, get_template_path

DEFAULT_BASIC = json.loads(
    _read_template(get_template_path(), "n2a-basic.json", "", ""))


def basic_model(model_id, name, css, qfmt, afmt):
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
        qfmt = DEFAULT_BASIC.get('front')
    if afmt is None:
        afmt = DEFAULT_BASIC.get('back')

    return Model(model_id, name,
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
