from dotenv import load_dotenv
load_dotenv()  # to załaduje zmienne z .env do os.environ

import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Filip" in response.data
