import pytest

from contact_book import db


@pytest.fixture
def temporary_database(monkeypatch, tmp_path):
    database_path = tmp_path / "contacts.db"
    monkeypatch.setattr(db, "DB_Path", database_path)
    return database_path
