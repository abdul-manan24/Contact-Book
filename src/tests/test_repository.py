from contact_book import repository
from contact_book.models import Contact


def test_repository_crud_and_count(temporary_database):
    contact = Contact(
        id=None,
        name="Ada Lovelace",
        phone="1234567890",
        email="ada@example.com",
        address="London",
        notes="Analytical engine",
        created_at="",
        updated_at="",
    )

    contact_id = repository.insert_record(contact)
    inserted = repository.fetch_one_record(contact_id)

    assert inserted["name"] == "Ada Lovelace"
    assert inserted["phone"] == "1234567890"
    assert len(repository.fetch_all_records()) == 1
    assert repository.count_records(None)[0][0] == 1

    assert repository.update_record(
        "name = ?, updated_at = ?", ("Augusta King", "2026-01-01", contact_id)
    ) == 1
    assert repository.fetch_one_record(contact_id)["name"] == "Augusta King"

    assert repository.delete_record(contact_id) == 1
    assert repository.fetch_one_record(contact_id) is None
    assert repository.count_records(None)[0][0] == 0


def test_fetch_all_records_applies_limit_and_offset(temporary_database):
    for name in ("Ada Lovelace", "Grace Hopper", "Katherine Johnson"):
        repository.insert_record(Contact(
            id=None,
            name=name,
            phone="1234567890",
            email=None,
            address=None,
            notes=None,
            created_at="",
            updated_at="",
        ))

    records = repository.fetch_all_records(limit=1, offset=1)

    assert [record["name"] for record in records] == ["Grace Hopper"]