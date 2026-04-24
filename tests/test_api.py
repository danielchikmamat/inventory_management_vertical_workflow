"""Tests for FastAPI endpoints in the inventory management system"""
from sqlite3 import Connection

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, ANY
from main import app
from app.schemas import Item, ItemUpdate, ItemFilter
from app.exceptions import ItemNotFoundError, DuplicateItemError
from app.db.connection import get_db_connection
from app.repo.model import DeleteResult


@pytest.fixture
def client(test_db: Connection):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass  # don't close here, fixture handles it

    app.dependency_overrides[get_db_connection] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def sample_item():
    """Fixture for a sample item"""
    return {
        "id": 1,
        "name": "Test Item",
        "price": 99.99,
        "quantity": 10
    }


@pytest.fixture
def sample_item_list():
    """Fixture for a list of sample items"""
    return [
        {
            "id": 1,
            "name": "Item 1",
            "price": 10.0,
            "quantity": 5
        },
        {
            "id": 2,
            "name": "Item 2",
            "price": 20.0,
            "quantity": 15
        }
    ]


class TestRootEndpoint:
    """Tests for the root endpoint"""

    def test_read_root(self, client: TestClient):
        """Test root endpoint returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the Inventory Management API"}


class TestCreateItem:
    """Tests for POST /items/ endpoint"""

    @patch('app.service.add_item')
    def test_create_item_success(self, mock_add_item, client: TestClient, sample_item: dict[str, Any]):
        """Test successful item creation"""
        mock_add_item.return_value = sample_item

        item_data = {
            "name": "Test Item",
            "price": 99.99,
            "quantity": 10
        }

        response = client.post("/items/", json=item_data)

        assert response.status_code == 201
        assert response.json() == sample_item
        mock_add_item.assert_called_once()

    @patch('app.service.add_item')
    def test_create_item_duplicate_error(self, mock_add_item, client: TestClient):
        """Test item creation with duplicate name"""
        mock_add_item.side_effect = DuplicateItemError("Item with this name already exists")

        item_data = {
            "name": "Duplicate Item",
            "price": 50.0,
            "quantity": 5
        }

        response = client.post("/items/", json=item_data)

        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    def test_create_item_invalid_data(self, client: TestClient):
        """Test item creation with invalid data"""
        item_data = {
            "name": "Test",
            "price": "invalid_price",  # Should be a number
            "quantity": 10
        }

        response = client.post("/items/", json=item_data)
        assert response.status_code == 422  # Validation error


class TestGetItems:
    """Tests for GET /items/ endpoint"""

    @patch('app.service.get_items_filtered')
    def test_get_items_no_filters(self, mock_get_items, client: TestClient, sample_item_list: list[dict[str, Any]]):
        """Test getting all items without filters"""
        mock_get_items.return_value = sample_item_list

        response = client.get("/items/")

        assert response.status_code == 200
        assert response.json() == sample_item_list



    @patch('app.service.get_items_filtered')
    def test_get_items_with_threshold(self, mock_get_items, client: TestClient, sample_item_list: list[dict[str, Any]]):
        """Test getting items with quantity threshold filter"""
        filtered_items = [sample_item_list[1]]  # Only item with quantity > 10
        mock_get_items.return_value = filtered_items

        response = client.get("/items/?threshold=10")

        assert response.status_code == 200
        assert response.json() == filtered_items


    @patch('app.service.get_items_filtered')
    def test_get_items_with_price_range(self, mock_get_items, client: TestClient, sample_item_list: list[dict[str, Any]]):
        """Test getting items with price range filters"""
        mock_get_items.return_value = sample_item_list

        response = client.get("/items/?min_price=5.0&max_price=25.0")

        assert response.status_code == 200
        assert response.json() == sample_item_list

    @patch('app.service.get_items_filtered')
    def test_get_items_all_filters(self, mock_get_items, client: TestClient):
        """Test getting items with all filters applied"""
        mock_get_items.return_value = []

        response = client.get("/items/?threshold=10&min_price=5.0&max_price=100.0")

        assert response.status_code == 200
        assert response.json() == []



class TestGetItemById:
    """Tests for GET /items/{item_id} endpoint"""

    @patch('app.service.get_item_by_id')
    def test_fetch_item_by_id_success(self, mock_get_item, client: TestClient, sample_item: dict[str, Any]):
        """Test successfully fetching an item by ID"""
        mock_get_item.return_value = sample_item

        response = client.get("/items/1")

        assert response.status_code == 200
        assert response.json() == sample_item
        mock_get_item.assert_called_once_with(ANY, 1)

    @patch('app.service.get_item_by_id')
    def test_fetch_item_by_id_not_found(self, mock_get_item, client: TestClient):
        """Test fetching non-existent item"""
        mock_get_item.side_effect = ItemNotFoundError("Item not found")

        response = client.get("/items/999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_fetch_item_invalid_id(self, client: TestClient):
        """Test fetching item with invalid ID format"""
        response = client.get("/items/invalid")
        assert response.status_code == 422  # Validation error


class TestUpdateItem:
    """Tests for PUT /items/{item_id} endpoint"""

    @patch('app.service.update_item')
    def test_update_item_success(self, mock_update_item, client: TestClient, sample_item: dict[str, Any]):
        """Test successful item update"""
        updated_item = {**sample_item, "name": "Updated Item", "price": 150.0}
        mock_update_item.return_value = updated_item

        update_data = {
            "name": "Updated Item",
            "price": 150.0
        }

        response = client.put("/items/1", json=update_data)

        assert response.status_code == 200
        assert response.json()["name"] == "Updated Item"
        assert response.json()["price"] == 150.0

    @patch('app.service.update_item')
    def test_update_item_not_found(self, mock_update_item, client: TestClient):
        """Test updating non-existent item"""
        mock_update_item.side_effect = ItemNotFoundError("Item not found")

        update_data = {"name": "Updated Name"}
        response = client.put("/items/999", json=update_data)

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    @patch('app.service.update_item')
    def test_update_item_partial(self, mock_update_item, client: TestClient, sample_item: dict[str, Any]):
        """Test partial item update"""
        updated_item = {**sample_item, "quantity": 20}
        mock_update_item.return_value = updated_item

        update_data = {"quantity": 20}
        response = client.put("/items/1", json=update_data)

        assert response.status_code == 200
        assert response.json()["quantity"] == 20

    def test_update_item_invalid_data(self, client: TestClient):
        """Test updating item with invalid data"""
        update_data = {"price": "invalid"}
        response = client.put("/items/1", json=update_data)

        assert response.status_code == 422

    def test_update_item_no_data_provided(self, client: TestClient):

         update_data = {}
         response = client.put("/items/1", json=update_data)
         assert response.status_code == 400


class TestDeleteItem:
    """Tests for DELETE /items/{item_id} endpoint"""

    @patch('app.service.delete_item')
    def test_delete_item_success(self, mock_delete_item, client: TestClient):
        """Test successful item deletion"""
        mock_delete_item.return_value = {"id": 1, "name": "Widget"}

        response = client.delete("/items/1")

        assert response.status_code == 200
        assert response.json() == {"id": 1, "name": "Widget"}
        mock_delete_item.assert_called_once_with(ANY, 1)

    @patch("app.service.delete_item")
    def test_delete_item_not_found(self, mock_delete_item, client: TestClient):
        mock_delete_item.side_effect = ItemNotFoundError("Item not found")

        response = client.delete("/items/999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


    def test_delete_item_invalid_id(self, client: TestClient):
        """Test deleting item with invalid ID"""
        response = client.delete("/items/invalid")
        assert response.status_code == 422


class TestStockValueMetrics:
    """Tests for GET /metrics/stock-value endpoint"""

    @patch('app.service.stock_value')
    def test_get_stock_value_success(self, mock_stock_value, client: TestClient):
        """Test getting total stock value"""
        mock_stock_value.return_value = {"total_value": 1500.50}

        response = client.get("/metrics/stock-value")

        assert response.status_code == 200
        assert response.json() == {"total_value": 1500.50}
        mock_stock_value.assert_called_once()

    @patch('app.service.stock_value')
    def test_get_stock_value_empty_inventory(self, mock_stock_value, client: TestClient):
        """Test getting stock value with no items"""
        mock_stock_value.return_value = {"total_value": 0.0}

        response = client.get("/metrics/stock-value")

        assert response.status_code == 200
        assert response.json() == {"total_value": 0.0}


# Integration-style tests (optional - if you want to test with real DB)
class TestEndpointIntegration:
    """Integration tests for endpoints with database"""

    @pytest.mark.integration
    def test_create_and_get_item_flow(self, client: TestClient):
        """Test creating an item and then retrieving it"""
        # This would use a test database
        # Create item
        item_data = {
            "name": f"Integration Test Item",
            "price": 10.0,
            "quantity": 5
        }

        create_response = client.post("/items/", json=item_data)
        assert create_response.status_code == 201

        item_id = create_response.json()["id"]

        # Get item
        get_response = client.get(f"/items/{item_id}")
        assert get_response.status_code == 200
        assert get_response.json()["name"] == item_data["name"]


# Pytest configuration for running specific test groups
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests (deselect with '-m \"not integration\"')"
    )