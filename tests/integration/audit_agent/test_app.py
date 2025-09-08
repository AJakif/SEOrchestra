import pytest
from fastapi.testclient import TestClient
from audit_agent.src.app import app

@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)

def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "SEO Audit Agent"}

def test_crawl_and_audit_invalid_url(client):
    """Test the crawl-and-audit endpoint with an invalid URL"""
    response = client.post("/crawl-and-audit", json={"url": "not-a-valid-url", "max_pages": 1})
    assert response.status_code == 500
    assert "Audit failed" in response.json()["detail"]

# Note: More comprehensive integration tests would require mocking the crawler
# and SEO checker, which we'll implement in a more advanced test setup