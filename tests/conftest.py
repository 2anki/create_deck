import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from typing import Generator

from twoanki.main import app
from twoanki.services.memory_service import MemoryService

@pytest.fixture
def client() -> Generator:
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def mock_memory_service():
    return AsyncMock(spec=MemoryService)

@pytest.fixture(autouse=True)
def setup_test_env():
    # This ensures we have a clean event loop for each test
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close() 