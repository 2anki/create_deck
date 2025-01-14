import os
import tempfile
from unittest import TestCase, mock
from genanki import Note, Model

from helpers.write_apkg import sanitize_filename, _write_new_apkg

class TestWriteApkg(TestCase):
    def setUp(self):
        self.test_model = Model(
            1607392319,
            'Test Model',
            [{'name': 'Question'}, {'name': 'Answer'}],
            [{'name': 'Card 1', 'qfmt': '{{Question}}', 'afmt': '{{Answer}}'}]
        )
        
    def test_sanitize_filename(self):
        test_cases = [
            ("Hello World!", "Hello-World"),
            ("Test@#$%^&*", "Test"),
            ("Space - Dash", "Space---Dash"),
            ("emoji😀test", "emoji😀test"),
            ("", "")
        ]
        
        for input_name, expected in test_cases:
            self.assertEqual(sanitize_filename(input_name), expected)

    @mock.patch('helpers.write_apkg.Package')
    @mock.patch('os.rename')
    def test_write_new_apkg_single_deck(self, mock_rename, mock_package):
        note = Note(model=self.test_model, fields=['Q1', 'A1'])
        deck_payload = {
            "id": 1234567890,
            "name": "Test Deck",
            "desc": "Test Description",
            "notes": [note]
        }
        
        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch('os.getcwd', return_value=tmpdir):
                _write_new_apkg([deck_payload], [])
                
                # Verify Package was created with correct deck
                mock_package.assert_called_once()
                created_deck = mock_package.call_args[0][0][0]
                self.assertEqual(created_deck.name, "Test Deck")
                self.assertEqual(str(created_deck.deck_id), "1234567890")
                
                # Verify file operations
                mock_package.return_value.write_to_file.assert_called_once()
                mock_rename.assert_called_once()

    @mock.patch('helpers.write_apkg.Package')
    @mock.patch('os.rename')
    def test_write_new_apkg_multiple_decks(self, mock_rename, mock_package):
        note1 = Note(model=self.test_model, fields=['Q1', 'A1'])
        note2 = Note(model=self.test_model, fields=['Q2', 'A2'])
        
        deck_payloads = [
            {
                "id": 1234567890,
                "name": "Test Deck 1",
                "desc": "Test Description 1",
                "notes": [note1]
            },
            {
                "id": 9876543210,
                "name": "Test Deck 2",
                "desc": "Test Description 2",
                "notes": [note2]
            }
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch('os.getcwd', return_value=tmpdir):
                _write_new_apkg(deck_payloads, [])
                
                mock_package.assert_called_once()
                created_decks = mock_package.call_args[0][0]
                self.assertEqual(len(created_decks), 2)
                self.assertEqual(created_decks[0].name, "Test Deck 1")
                self.assertEqual(created_decks[1].name, "Test Deck 2")
                
                # Verify file operations
                mock_package.return_value.write_to_file.assert_called_once()
                mock_rename.assert_called_once()

    @mock.patch('helpers.write_apkg.Package')
    @mock.patch('os.rename')
    def test_write_new_apkg_with_media(self, mock_rename, mock_package):
        note = Note(model=self.test_model, fields=['Q1', 'A1'])
        deck_payload = {
            "id": 1234567890,
            "name": "Test Deck",
            "desc": "Test Description",
            "notes": [note]
        }
        media_files = ['test.jpg', 'audio.mp3']
        
        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch('os.getcwd', return_value=tmpdir):
                _write_new_apkg([deck_payload], media_files)
                
                mock_package.assert_called_once()
                package_instance = mock_package.return_value
                self.assertEqual(package_instance.media_files, media_files)
                
                # Verify file operations
                mock_package.return_value.write_to_file.assert_called_once()
                mock_rename.assert_called_once()

    @mock.patch('helpers.write_apkg.Package')
    @mock.patch('os.rename')
    def test_write_new_apkg_empty_deck_list(self, mock_rename, mock_package):
        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch('os.getcwd', return_value=tmpdir):
                _write_new_apkg([], [])
                
                mock_package.assert_called_once()
                mock_package.return_value.write_to_file.assert_called_once()
                mock_rename.assert_called_once()
                
                # Verify the default name is used
                src, dst = mock_rename.call_args[0]
                self.assertTrue('default-' in dst) 