"""
Helper functions for working with the flashcards
"""
import ftfy


def get_safe_value(value):
    """
    Remove any surrogates in the value.
    :param value:
    :return:
    """
    return ftfy.fixes.fix_surrogates(value)
