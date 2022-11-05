import unittest
import os
import zipfile

from helpers.zip.zip import get_files_in_zip_file

EXAMPLE_ZIP_PATH = "create_deck-example.zip"
EXAMPLE_FILE_PATH = '/tmp/input.txt'


class MyTestCase(unittest.TestCase):
    def setUp(self):
        with open(EXAMPLE_FILE_PATH, 'w') as f:
            f.write('tull')
        filepath = os.path.join(os.getcwd(), EXAMPLE_ZIP_PATH)
        with zipfile.ZipFile(filepath, 'a') as zipf:
            zipf.write(EXAMPLE_ZIP_PATH, "input.txt")

    def tearDown(self):
        os.remove(EXAMPLE_ZIP_PATH)
        os.remove(EXAMPLE_FILE_PATH)

    def test_get_files(self):
        expect_files = ['input.txt']
        actual_files = get_files_in_zip_file(EXAMPLE_ZIP_PATH)
        self.assertEqual(expect_files, actual_files)


if __name__ == '__main__':
    unittest.main()
