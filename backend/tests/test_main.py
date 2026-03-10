import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    """测试健康检查"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"

def test_get_api_config(client):
    """测试获取 API 配置"""
    response = client.get("/api/v1/api-config")
    assert response.status_code == 200

def test_get_recordings(client):
    """测试获取录音列表"""
    response = client.get("/api/v1/recordings")
    assert response.status_code == 200
    data = response.json()
    assert "recordings" in data
    assert isinstance(data["recordings"], list)

def test_get_models(client):
    """测试获取模型列表"""
    response = client.get("/api/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data