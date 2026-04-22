"""Pytest configuration and shared fixtures"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock


@pytest.fixture(autouse=True)
def mock_db_dependency(monkeypatch):
    """Automatically mock the database connection dependency for all tests"""
    mock_conn = Mock()

    def mock_get_db():
        return mock_conn

    # This prevents the real database connection from being called
    monkeypatch.setattr("src.db.connection.get_db_connection", mock_get_db)

    return mock_conn