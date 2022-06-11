"""
Load template file
"""
from helpers.get_path_start import _path_start


def _read_template(template_dir, path, fmt, value):
    file_path = path if path.startswith(_path_start()) else template_dir + path
    with open(file_path, "r", encoding="utf-8") as file:
        if fmt and value:
            return file.read().replace(fmt, value)
        return file.read()
