from helpers.read_template import _read_template


def get_styling(first_deck, template_dir, template_selection):
    """
    retrieve the styling for the user. The default is the notion style loaded in dynnamically.

    :param first_deck:
    :param template_dir:
    :param template_selection:
    :return:
    """
    styling = first_deck.get('style', '') or ''

    if template_selection == 'specialstyle':
        styling += _read_template(template_dir, "custom.css", "", "")
    elif template_selection == 'nostyle':
        styling = ""
    elif template_selection == 'abhiyan':
        styling = _read_template(template_dir, 'abhiyan.css', "", "")
    elif template_selection == 'alex_deluxe':
        styling = _read_template(template_dir, 'alex_deluxe.css', "", "")

    return styling
