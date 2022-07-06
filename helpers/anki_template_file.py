from helpers.get_model_id import get_model_id
from helpers.get_styling import get_styling
from helpers.read_template import _read_template


class AnkiTemplateFile:
    id = 0
    name = ""
    front = ""
    back = ""
    style = ""

    def __init__(self, deck_settings, name, template_dir, template_selection):
        self.name = deck_settings.get(f'{name}ModelName',
                                      f'n2a-{name}' or f'n2a-{name}')
        self.id = deck_settings.get(f'{name}ModelId', get_model_id(self.name))
        self.style = get_styling(deck_settings, template_dir,
                                 template_selection)
        self.front = None
        self.back = None

    def override_values(self, custom_template):
        """
        Read values from custom template.
        :param custom_template:
        :return:
        """
        if custom_template:
            self.style = custom_template["styling"]
            self.front = custom_template["front"]
            self.back = custom_template["back"]

    def load_user_file(self, template_dir, user_name):
        """
        Read custom template based on user name
        :param template_dir:
        :param user_name:
        :return:
        """
        self.style = _read_template(template_dir,
                                    f"{user_name}_cloze_style.css", "", "")
        self.front = _read_template(template_dir,
                                    f"{user_name}_cloze_front.html",
                                    "", "")
        self.back = _read_template(template_dir,
                                   f"{user_name}_cloze_back.html",
                                   "", "")

    def clear_style(self):
        """
        Remove the template style
        :return:
        """
        self.style = ''
