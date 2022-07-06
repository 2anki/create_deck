"""
Testing the deck creation function
"""
import os.path

from pytest import raises

from create_deck import create_deck


def test_fails_on_no_arguments():
    """
    Test the script fails on missing input.
    """
    with raises(IOError):
        create_deck(None, None)


def test_passes_with_valid_arguments(capsys):
    """
    Test APKG is generated with valid arguments
    :return:
    """
    workspace_dir = os.path.dirname(__file__) + "/artifacts/deck_info.json"
    template_dir = os.path.dirname(__file__) + "/artifacts/workspace/templates/"
    create_deck(workspace_dir, template_dir)
    captured = capsys.readouterr()
    assert "2397113444128748.apkg" in captured.out
