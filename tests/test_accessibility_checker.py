from app import create_app
import pytest
import app.services as ar

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_analyze_success(client, monkeypatch):
    # --- Mocked axe result ---
    fake_result = {
        "violations": [
            {
                "id": "color-contrast",
                "impact": "serious",
                "description": "Contrast issue",
                "nodes": [{"html": "<h1>Hello</h1>"}]
            },
            {
                "id": "alt-text",
                "impact": "critical",
                "description": "Missing alt attribute",
                "nodes": [{"html": "<img src='logo.png'>"}]
            }
        ]
    }

    # --- Replace run_axe_analysis with fake one ---
    def fake_run_axe_analysis(url):
        return fake_result

    monkeypatch.setattr(ar, "run_axe_analysis", fake_run_axe_analysis)

    # --- Call endpoint ---
    response = client.get("/analyze?url=https://example.com")
    data = response.get_json()

    assert response.status_code == 200
    assert data["summary"]["total_issues"] == 2
    assert "by_impact" in data
    assert data["summary"]["by_impact"]["serious"] == 1
    assert data["summary"]["by_impact"]["critical"] == 1


def test_analyze_missing_url(client):
    response = client.get("/analyze")
    data = response.get_json()

    assert response.status_code == 400
    assert "error" in data


def test_analyze_failure(client, monkeypatch):
    # --- Mock exception ---
    def fake_run_axe_analysis(url):
        raise RuntimeError("Playwright error")

    monkeypatch.setattr(ar, "run_axe_analysis", fake_run_axe_analysis)

    response = client.get("/analyze?url=https://example.com")
    data = response.get_json()

    assert response.status_code == 500
    assert "error" in data
