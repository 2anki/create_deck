import pytest
from fastapi.testclient import TestClient
from twoanki.main import app

def test_create_deck_success(client: TestClient):
    test_payload = {
        "deck": {
            "name": "Test Deck",
            "cards": [
                {
                    "front": "Question 1",
                    "back": "Answer 1",
                    "tags": ["test"],
                    "cloze": False,
                    "enable_input": False,
                    "media": []
                }
            ],
            "settings": {
                "use_input": False,
                "max_one": True,
                "no_underline": False,
                "template": "specialstyle"
            }
        }
    }

    response = client.post("/api/v1/decks", json=test_payload)
    assert response.status_code == 200
    assert "deck_id" in response.json()
    assert "download_url" in response.json()

def test_create_deck_invalid_data(client: TestClient):
    invalid_payload = {
        "deck": {
            "name": "",  # Invalid: empty name
            "cards": []  # Invalid: no cards
        }
    }

    response = client.post("/api/v1/decks", json=invalid_payload)
    assert response.status_code == 400 