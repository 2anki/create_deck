import unittest
import os
import zipfile

from helpers.zip.zip import get_files_in_zip_file, get_text_in_zip_file

EXAMPLE_ZIP_PATH = "create_deck-example.zip"


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        filepath = os.path.join(os.getcwd(), EXAMPLE_ZIP_PATH)
        with zipfile.ZipFile(filepath, 'a') as zipf:
            zipf.writestr("input.txt", 'tull')

    @classmethod
    def tearDownClass(cls):
        os.remove(EXAMPLE_ZIP_PATH)

    def test_get_files(self):
        expect_files = ['input.txt']
        actual_files = get_files_in_zip_file(EXAMPLE_ZIP_PATH)
        self.assertEqual(expect_files, actual_files)

    def test_get_text_content(self):
        expected = "tull"
        actual = get_text_in_zip_file(EXAMPLE_ZIP_PATH, "input.txt")
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
