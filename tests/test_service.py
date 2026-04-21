"""
Tests for inventory management service layer (service.py).
Repository is mocked so no DB is required.
"""
import sqlite3
import pytest
from unittest.mock import patch, MagicMock
from types import SimpleNamespace

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_item_data(name="Widget", quantity=10, price=9.99):
    return SimpleNamespace(name=name, quantity=quantity, price=price)

def make_db_item(id=1, name="Widget", quantity=10, price=9.99):
    return {"id": id, "name": name, "quantity": quantity, "price": price}


# ---------------------------------------------------------------------------
# Patch target – all tests patch 'src.service.repo'
# ---------------------------------------------------------------------------

REPO = "src.service.repo"


# ===========================================================================
# get_items_filtered
# ===========================================================================

class TestGetItemsFiltered:

    def test_no_filters_returns_all(self):
        items = [make_db_item(1), make_db_item(2, name="Gadget")]
        with patch(REPO) as mock_repo:
            mock_repo.get_items_filtered.return_value = items
            from src.service import get_items_filtered
            result = get_items_filtered()
        mock_repo.get_items_filtered.assert_called_once_with(None, None, None)
        assert result == items

    def test_threshold_filter_forwarded(self):
        with patch(REPO) as mock_repo:
            mock_repo.get_items_filtered.return_value = []
            from src.service import get_items_filtered
            get_items_filtered(threshold=5)
        mock_repo.get_items_filtered.assert_called_once_with(5, None, None)

    def test_price_range_filter_forwarded(self):
        with patch(REPO) as mock_repo:
            mock_repo.get_items_filtered.return_value = []
            from src.service import get_items_filtered
            get_items_filtered(min_price=1.0, max_price=50.0)
        mock_repo.get_items_filtered.assert_called_once_with(None, 1.0, 50.0)

    def test_all_filters_forwarded(self):
        with patch(REPO) as mock_repo:
            mock_repo.get_items_filtered.return_value = []
            from src.service import get_items_filtered
            get_items_filtered(threshold=3, min_price=2.0, max_price=100.0)
        mock_repo.get_items_filtered.assert_called_once_with(3, 2.0, 100.0)

    def test_returns_empty_list_when_no_matches(self):
        with patch(REPO) as mock_repo:
            mock_repo.get_items_filtered.return_value = []
            from src.service import get_items_filtered
            result = get_items_filtered(threshold=1)
        assert result == []


# ===========================================================================
# add_item
# ===========================================================================

class TestAddItem:

    def test_returns_item_dict_on_success(self):
        item_data = make_item_data()
        with patch(REPO) as mock_repo:
            mock_repo.add_data.return_value = 42
            from src.service import add_item
            result = add_item(item_data)
        assert result == {"id": 42, "name": "Widget", "quantity": 10, "price": 9.99}

    def test_calls_repo_with_correct_args(self):
        item_data = make_item_data(name="Bolt", quantity=100, price=0.05)
        with patch(REPO) as mock_repo:
            mock_repo.add_data.return_value = 7
            from src.service import add_item
            add_item(item_data)
        mock_repo.add_data.assert_called_once_with("Bolt", 100, 0.05)

    def test_raises_duplicate_error_on_integrity_error(self):
        from src.exceptions import DuplicateItemError
        item_data = make_item_data()
        with patch(REPO) as mock_repo:
            mock_repo.add_data.side_effect = sqlite3.IntegrityError
            from src.service import add_item
            with pytest.raises(DuplicateItemError, match="item already exists"):
                add_item(item_data)

    def test_zero_quantity_accepted(self):
        item_data = make_item_data(quantity=0)
        with patch(REPO) as mock_repo:
            mock_repo.add_data.return_value = 5
            from src.service import add_item
            result = add_item(item_data)
        assert result["quantity"] == 0

    def test_zero_price_accepted(self):
        item_data = make_item_data(price=0.0)
        with patch(REPO) as mock_repo:
            mock_repo.add_data.return_value = 6
            from src.service import add_item
            result = add_item(item_data)
        assert result["price"] == 0.0


# ===========================================================================
# get_item_by_id
# ===========================================================================

class TestGetItemById:

    def test_returns_item_when_found(self):
        item = make_db_item()
        with patch(REPO) as mock_repo:
            mock_repo.get_item_by_id.return_value = item
            from src.service import get_item_by_id
            result = get_item_by_id(1)
        assert result == item

    def test_raises_item_not_found_when_missing(self):
        from src.exceptions import ItemNotFoundError
        with patch(REPO) as mock_repo:
            mock_repo.get_item_by_id.return_value = None
            from src.service import get_item_by_id
            with pytest.raises(ItemNotFoundError, match="Item 99 not found"):
                get_item_by_id(99)

    def test_calls_repo_with_correct_id(self):
        with patch(REPO) as mock_repo:
            mock_repo.get_item_by_id.return_value = make_db_item()
            from src.service import get_item_by_id
            get_item_by_id(7)
        mock_repo.get_item_by_id.assert_called_once_with(7)


# ===========================================================================
# update_item
# ===========================================================================

class TestUpdateItem:

    def test_successful_update_returns_repo_result(self):
        item_update = make_item_data(name="Updated Widget", quantity=20, price=14.99)
        with patch(REPO) as mock_repo:
            mock_repo.get_item_by_id.return_value = make_db_item()
            mock_repo.item_name_exists.return_value = False
            mock_repo.update_item.return_value = True
            from src.service import update_item
            result = update_item(1, item_update)
        assert result is True

    def test_raises_not_found_when_item_missing(self):
        from src.exceptions import ItemNotFoundError
        item_update = make_item_data()
        with patch(REPO) as mock_repo:
            mock_repo.get_item_by_id.return_value = None
            from src.service import update_item
            with pytest.raises(ItemNotFoundError):
                update_item(99, item_update)

    def test_raises_duplicate_when_name_taken(self):
        from src.exceptions import DuplicateItemError
        item_update = make_item_data(name="Taken Name")
        with patch(REPO) as mock_repo:
            mock_repo.get_item_by_id.return_value = make_db_item()
            mock_repo.item_name_exists.return_value = True
            from src.service import update_item
            with pytest.raises(DuplicateItemError):
                update_item(1, item_update)

    def test_repo_update_called_with_correct_args(self):
        item_update = make_item_data(name="New Name", quantity=5, price=3.50)
        with patch(REPO) as mock_repo:
            mock_repo.get_item_by_id.return_value = make_db_item()
            mock_repo.item_name_exists.return_value = False
            mock_repo.update_item.return_value = True
            from src.service import update_item
            update_item(1, item_update)
        mock_repo.update_item.assert_called_once_with(
            1, name="New Name", quantity=5, price=3.50
        )

    def test_name_uniqueness_check_is_called(self):
        item_update = make_item_data(name="SomeName")
        with patch(REPO) as mock_repo:
            mock_repo.get_item_by_id.return_value = make_db_item()
            mock_repo.item_name_exists.return_value = False
            mock_repo.update_item.return_value = True
            from src.service import update_item
            update_item(1, item_update)
        mock_repo.item_name_exists.assert_called_once_with("SomeName")


# ===========================================================================
# delete_item
# ===========================================================================

class TestDeleteItem:

    def test_returns_true_when_deleted(self):
        with patch(REPO) as mock_repo:
            mock_repo.delete_item.return_value = True
            from src.service import delete_item
            assert delete_item(1) is True

    def test_returns_false_when_not_found(self):
        with patch(REPO) as mock_repo:
            mock_repo.delete_item.return_value = False
            from src.service import delete_item
            assert delete_item(999) is False

    def test_calls_repo_with_correct_id(self):
        with patch(REPO) as mock_repo:
            mock_repo.delete_item.return_value = True
            from src.service import delete_item
            delete_item(42)
        mock_repo.delete_item.assert_called_once_with(42)


# ===========================================================================
# stock_value
# ===========================================================================

class TestStockValue:

    def test_returns_wrapped_total(self):
        with patch(REPO) as mock_repo:
            mock_repo.stock_value.return_value = 1234.56
            from src.service import stock_value
            result = stock_value()
        assert result == {"total_stock_value": 1234.56}

    def test_returns_zero_when_no_stock(self):
        with patch(REPO) as mock_repo:
            mock_repo.stock_value.return_value = 0
            from src.service import stock_value
            result = stock_value()
        assert result == {"total_stock_value": 0}

    def test_calls_repo_stock_value(self):
        with patch(REPO) as mock_repo:
            mock_repo.stock_value.return_value = 0
            from src.service import stock_value
            stock_value()
        mock_repo.stock_value.assert_called_once()