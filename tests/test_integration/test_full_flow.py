import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from twoanki.main import app

@pytest.mark.integration
def test_full_deck_creation_flow():
    with TestClient(app) as client:
        # Create deck
        create_payload = {
            "deck": {
                "name": "Integration Test Deck",
                "cards": [
                    {
                        "front": "Question 1",
                        "back": "Answer 1",
                        "tags": ["integration"]
                    }
                ],
                "settings": {
                    "use_input": False,
                    "max_one": True
                }
            }
        }
        
        response = client.post("/api/v1/decks", json=create_payload)
        assert response.status_code == 200
        deck_id = response.json()["deck_id"]
        
        # Verify deck creation
        get_response = client.get(f"/api/v1/decks/{deck_id}")
        assert get_response.status_code == 200
        assert get_response.json()["name"] == "Integration Test Deck"
        
        # Download deck
        download_response = client.get(f"/api/v1/decks/{deck_id}/download")
        assert download_response.status_code == 200
        assert download_response.headers["content-type"] == "application/octet-stream" 