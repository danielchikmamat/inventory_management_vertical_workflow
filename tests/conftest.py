"""Pytest configuration and shared fixtures"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock
import os
import sqlite3 as sqlite3
from pathlib import Path

os.environ["ENV"] = "test"

@pytest.fixture
def test_db():
    """
    Fresh in-memory SQLite DB for each test.
    that each try to close it internally.
    """
    schema = Path("src/db/schema.sql").read_text()

    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row

    conn.executescript(schema)
    conn.commit()

    yield conn

    conn.close()
