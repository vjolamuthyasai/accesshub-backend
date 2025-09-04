import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_analyze_no_url(client):
    response = client.get("/analyze")
    assert response.status_code == 400
    assert b"Please provide a URL" in response.data

def test_analyze_with_html(client, monkeypatch):
    # Mock requests.get to return custom HTML
    import requests
    class MockResponse:
        status_code = 200
        text = "<html><head><title></title></head><body><h1>Hello</h1></body></html>"
        def raise_for_status(self): pass
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: MockResponse())

    response = client.get("/analyze?url=http://fake.com")
    data = response.get_json()
    assert response.status_code == 200
    assert data["summary"]["high"] == 1
    assert "missing_title" in [i["type"] for i in data["issues"]]

def test_pdf_generation(client, monkeypatch):
    # Mock requests.get
    import requests
    class MockResponse:
        status_code = 200
        text = "<html><head><title>PDF</title></head><body><h1>Ok</h1></body></html>"
        def raise_for_status(self): pass
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: MockResponse())

    response = client.get("/analyze/pdf?url=http://fake.com")
    assert response.status_code == 200
    assert response.mimetype == "application/pdf"
