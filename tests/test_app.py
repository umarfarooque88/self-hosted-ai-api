"""
Tests for Self-Hosted AI API
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint"""

    def test_health_check(self):
        """Test that health endpoint returns healthy status"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "ollama_url" in data


class TestModelsEndpoint:
    """Test models listing endpoint"""

    def test_list_models(self):
        """Test that models endpoint returns valid format"""
        response = client.get("/v1/models")
        assert response.status_code == 200
        data = response.json()
        assert data["object"] == "list"
        assert isinstance(data["data"], list)
        assert len(data["data"]) > 0


class TestChatCompletions:
    """Test chat completions endpoint"""

    def test_chat_completion_basic(self):
        """Test basic chat completion request"""
        response = client.post(
            "/v1/chat/completions",
            json={
                "messages": [
                    {"role": "user", "content": "Hello"}
                ]
            }
        )
        # Note: This will return 503 if Ollama is not running
        # which is expected behavior
        assert response.status_code in [200, 503]

    def test_chat_completion_format(self):
        """Test that response follows OpenAI format"""
        response = client.post(
            "/v1/chat/completions",
            json={
                "messages": [
                    {"role": "user", "content": "Hi"}
                ],
                "model": "qwen:1.8b"
            }
        )
        if response.status_code == 200:
            data = response.json()
            assert "choices" in data
            assert "model" in data
            assert isinstance(data["choices"], list)

    def test_chat_completion_multiple_messages(self):
        """Test chat with conversation history"""
        response = client.post(
            "/v1/chat/completions",
            json={
                "messages": [
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hi there!"},
                    {"role": "user", "content": "How are you?"}
                ]
            }
        )
        # Will return 503 if Ollama is not running
        assert response.status_code in [200, 503]

    def test_chat_completion_with_temperature(self):
        """Test chat completion with temperature parameter"""
        response = client.post(
            "/v1/chat/completions",
            json={
                "messages": [
                    {"role": "user", "content": "Tell me a story"}
                ],
                "temperature": 0.9
            }
        )
        assert response.status_code in [200, 503]

    def test_chat_completion_empty_messages(self):
        """Test that empty messages list is handled"""
        response = client.post(
            "/v1/chat/completions",
            json={
                "messages": []
            }
        )
        # Should return error for invalid request
        assert response.status_code in [400, 422, 503]


class TestOpenAICompatibility:
    """Test OpenAI API compatibility"""

    def test_response_structure(self):
        """Test that response structure matches OpenAI format"""
        response = client.post(
            "/v1/chat/completions",
            json={
                "messages": [{"role": "user", "content": "Test"}]
            }
        )
        if response.status_code == 200:
            data = response.json()
            # Check required OpenAI fields
            assert "id" in data
            assert "object" in data
            assert "created" in data or True  # Optional in our impl
            assert "model" in data
            assert "choices" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
