import mongomock
import pytest

@pytest.fixture
def mock_db():
    client = mongomock.MongoClient()
    return client['telegram_bot']