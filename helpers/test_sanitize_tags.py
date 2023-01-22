from helpers.sanitize_tags import sanitize_tags


def test_sanitize_tags():
    assert (sanitize_tags({'a  a'}) == ['a--a'])
