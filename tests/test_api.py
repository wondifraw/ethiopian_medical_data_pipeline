import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_get_messages():
    response = client.get("/messages/")
    assert response.status_code == 200

def test_get_channels():
    response = client.get("/channels/")
    assert response.status_code == 200

def test_get_image_detections():
    response = client.get("/image-detections/")
    assert response.status_code == 200 