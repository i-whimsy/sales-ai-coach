import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    """测试健康检查"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_config(client):
    """测试获取配置"""
    response = client.get("/api/config")
    assert response.status_code == 200
    data = response.json()
    assert "api_keys" in data
    assert "openai" in data["api_keys"]
    assert "claude" in data["api_keys"]
    assert "deepseek" in data["api_keys"]
    assert "whisper" in data["api_keys"]

def test_empty_recordings(client):
    """测试空记录列表"""
    response = client.get("/api/recordings")
    assert response.status_code == 200
    data = response.json()
    assert "recordings" in data
    assert isinstance(data["recordings"], list)