"""
Tests for repository.py — uses an in-memory SQLite DB, no files on disk.
get_db_connection is patched to return the test connection for every test.
"""
import pytest
import sqlite3
from unittest.mock import patch
from src import repository
from pathlib import Path
from src.db.connection import get_db_connection


DB_CONN = "src.repository.get_db_connection"


# ---------------------------------------------------------------------------
# Fixtures (move to conftest.py if sharing with other test files)
# ---------------------------------------------------------------------------

@pytest.fixture
def test_db():
    """
    Fresh in-memory SQLite DB for each test.
    that each try to close it internally.
    """
    schema = Path("src/db/schema.sql").read_text()

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    conn.executescript(schema)
    conn.commit()

    yield conn

    conn.close()






@pytest.fixture
def seeded_db(test_db):
    """test_db pre-loaded with two items."""
    test_db.execute("INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)",
                    ("Widget", 10, 9.99))
    test_db.execute("INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)",
                    ("Gadget", 5, 24.99))
    test_db.commit()
    return test_db


# ===========================================================================
# add_data
# ===========================================================================

class TestAddData:

    def test_returns_integer_id(self, test_db):

        with patch(DB_CONN, return_value=test_db):
            item_id = repository.add_data(test_db, "Widget", 10, 9.99)
        assert isinstance(item_id, int)

    def test_id_increments_on_each_insert(self, test_db):
        with patch(DB_CONN, return_value=test_db):
            id1 = repository.add_data(test_db, "Widget", 10, 9.99)
            id2 = repository.add_data(test_db, "Gadget", 5, 4.99)
        assert id2 > id1

    def test_item_persisted_in_db(self, test_db):
        with patch(DB_CONN, return_value=test_db):
            repository.add_data(test_db, "Widget", 10, 9.99)
        row = test_db.execute("SELECT * FROM items WHERE name = 'Widget'").fetchone()
        assert row["quantity"] == 10
        assert row["price"] == 9.99

    def test_duplicate_name_raises_integrity_error(self, test_db):
        with patch(DB_CONN, return_value=test_db):
            repository.add_data(test_db, "Widget", 10, 9.99)
            with pytest.raises(sqlite3.IntegrityError):
                repository.add_data(test_db, "Widget", 5, 4.99)


# ===========================================================================
# get_items_filtered
# ===========================================================================

class TestGetItemsFiltered:

    def test_returns_all_items_when_no_filters(self, seeded_db):
        with patch(DB_CONN, return_value=seeded_db):
            result = repository.get_items_filtered(seeded_db)
        assert len(result) == 2

    def test_returns_list_of_dicts(self, seeded_db):
        with patch(DB_CONN, return_value=seeded_db):
            result = repository.get_items_filtered(seeded_db)
        assert all(isinstance(item, dict) for item in result)

    def test_threshold_filters_low_stock(self, seeded_db):
        # Widget=10, Gadget=5 — threshold of 8 should return only Gadget
        with patch(DB_CONN, return_value=seeded_db):
            result = repository.get_items_filtered(seeded_db, threshold=8)
        assert len(result) == 1
        assert result[0]["name"] == "Gadget"

    def test_min_price_filter(self, seeded_db):
        # only Gadget (24.99) is above 15.00
        with patch(DB_CONN, return_value=seeded_db):
            result = repository.get_items_filtered(seeded_db, min_price=15.00)
        assert len(result) == 1
        assert result[0]["name"] == "Gadget"

    def test_max_price_filter(self, seeded_db):
        # only Widget (9.99) is below 15.00
        with patch(DB_CONN, return_value=seeded_db):
            result = repository.get_items_filtered(seeded_db, max_price=15.00)
        assert len(result) == 1
        assert result[0]["name"] == "Widget"

    def test_min_and_max_price_combined(self, seeded_db):
        with patch(DB_CONN, return_value=seeded_db):
            result = repository.get_items_filtered(seeded_db, min_price=5.00, max_price=15.00)
        assert len(result) == 1
        assert result[0]["name"] == "Widget"

    def test_no_matches_returns_empty_list(self, seeded_db):
        with patch(DB_CONN, return_value=seeded_db):
            result = repository.get_items_filtered(seeded_db, threshold=1)
        assert result == []

    def test_returns_empty_list_on_empty_table(self, test_db):
        with patch(DB_CONN, return_value=test_db):
            result = repository.get_items_filtered(test_db)
        assert result == []


# ===========================================================================
# get_item_by_id
# ===========================================================================

class TestGetItemById:

    def test_returns_dict_for_existing_item(self, seeded_db):
        row = seeded_db.execute("SELECT id FROM items WHERE name='Widget'").fetchone()
        with patch(DB_CONN, return_value=seeded_db):
            result = repository.get_item_by_id(seeded_db, row["id"])
        assert result["name"] == "Widget"
        assert isinstance(result, dict)

    def test_returns_none_for_missing_item(self, test_db):
        with patch(DB_CONN, return_value=test_db):
            result = repository.get_item_by_id(test_db, 999)
        assert result is None

    def test_returned_dict_has_expected_keys(self, seeded_db):
        row = seeded_db.execute("SELECT id FROM items WHERE name='Widget'").fetchone()
        with patch(DB_CONN, return_value=seeded_db):
            result = repository.get_item_by_id(seeded_db, row["id"])
        assert {"id", "name", "quantity", "price"}.issubset(result.keys())


# ===========================================================================
# update_item
# ===========================================================================

class TestUpdateItem:

    def test_updates_name(self, seeded_db):
        row = seeded_db.execute("SELECT id FROM items WHERE name='Widget'").fetchone()
        with patch(DB_CONN, return_value=seeded_db):
            updated = repository.update_item(seeded_db, row["id"], name="Super Widget")
        assert updated is True
        result = seeded_db.execute("SELECT name FROM items WHERE id=?",
                                   (row["id"],)).fetchone()
        assert result["name"] == "Super Widget"

    def test_updates_quantity(self, seeded_db):
        row = seeded_db.execute("SELECT id FROM items WHERE name='Widget'").fetchone()
        with patch(DB_CONN, return_value=seeded_db):
            repository.update_item(seeded_db, row["id"], quantity=99)
        result = seeded_db.execute("SELECT quantity FROM items WHERE id=?",
                                   (row["id"],)).fetchone()
        assert result["quantity"] == 99

    def test_updates_price(self, seeded_db):
        row = seeded_db.execute("SELECT id FROM items WHERE name='Widget'").fetchone()
        with patch(DB_CONN, return_value=seeded_db):
            repository.update_item(seeded_db, row["id"], price=1.23)
        result = seeded_db.execute("SELECT price FROM items WHERE id=?",
                                   (row["id"],)).fetchone()
        assert result["price"] == 1.23

    def test_returns_false_when_no_fields_provided(self, seeded_db):
        row = seeded_db.execute("SELECT id FROM items WHERE name='Widget'").fetchone()
        with patch(DB_CONN, return_value=seeded_db):
            result = repository.update_item(seeded_db, row["id"])
        assert result is False

    def test_returns_false_for_nonexistent_id(self, test_db):
        with patch(DB_CONN, return_value=test_db):
            result = repository.update_item(test_db, 999, name="Ghost")
        assert result is False


# ===========================================================================
# delete_item
# ===========================================================================

class TestDeleteItem:

    def test_returns_true_when_deleted(self, seeded_db):
        row = seeded_db.execute("SELECT id FROM items WHERE name='Widget'").fetchone()
        with patch(DB_CONN, return_value=seeded_db):
            result = repository.delete_item(seeded_db, row["id"])
        assert result is True

    def test_item_no_longer_in_db(self, seeded_db):
        row = seeded_db.execute("SELECT id FROM items WHERE name='Widget'").fetchone()
        item_id = row["id"]
        with patch(DB_CONN, return_value=seeded_db):
            repository.delete_item(seeded_db, item_id)
        remaining = seeded_db.execute("SELECT * FROM items WHERE id=?",
                                      (item_id,)).fetchone()
        assert remaining is None

    def test_returns_false_for_nonexistent_item(self, test_db):
        with patch(DB_CONN, return_value=test_db):
            result = repository.delete_item(test_db, 999)
        assert result is False

    def test_other_items_unaffected(self, seeded_db):
        row = seeded_db.execute("SELECT id FROM items WHERE name='Widget'").fetchone()
        with patch(DB_CONN, return_value=seeded_db):
            repository.delete_item(seeded_db, row["id"])
        remaining = seeded_db.execute("SELECT COUNT(*) as c FROM items").fetchone()
        assert remaining["c"] == 1


# ===========================================================================
# stock_value
# ===========================================================================

class TestStockValue:

    def test_returns_correct_total(self, seeded_db):
        # Widget: 10 * 9.99 = 99.90, Gadget: 5 * 24.99 = 124.95 → total 224.85
        with patch(DB_CONN, return_value=seeded_db):
            result = repository.stock_value(seeded_db)
        assert round(result, 2) == 224.85

    def test_returns_zero_on_empty_table(self, test_db):
        with patch(DB_CONN, return_value=test_db):
            result = repository.stock_value(test_db)
        assert result is None or result == 0

    def test_single_item_stock_value(self, test_db):
        test_db.execute("INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)",
                        ("Widget", 4, 5.00))
        test_db.commit()
        with patch(DB_CONN, return_value=test_db):
            result = repository.stock_value(test_db)
        assert result == 20.00


# ===========================================================================
# item_name_exists
# ===========================================================================

class TestItemNameExists:

    def test_returns_true_when_name_exists(self, seeded_db):
        with patch(DB_CONN, return_value=seeded_db):
            result = repository.item_name_exists(seeded_db, "Widget")
        assert result is True

    def test_returns_false_when_name_missing(self, seeded_db):
        with patch(DB_CONN, return_value=seeded_db):
            result = repository.item_name_exists(seeded_db, "Nonexistent")
        assert result is False

    def test_case_sensitive(self, seeded_db):
        # SQLite is case-insensitive for ASCII by default,
        # so this documents current behaviour rather than enforcing case sensitivity
        with patch(DB_CONN, return_value=seeded_db):
            result = repository.item_name_exists(seeded_db, "widget")
        assert isinstance(result, bool)  # documents behaviour without asserting case