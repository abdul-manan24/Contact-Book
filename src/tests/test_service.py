from argparse import Namespace

from contact_book import repository, service


def test_add_contact_stores_contact_and_reports_success(
    temporary_database, capsys
):
    contact = Namespace(
        name="Ada Lovelace",
        phone="1234567890",
        email="ada@example.com",
        address=None,
        notes=None,
    )

    service.add_contact(contact)

    record = repository.fetch_one_record(1)
    assert record["name"] == "Ada Lovelace"
    assert record["email"] == "ada@example.com"
    assert "Contact inserted successfully! assigned id 1" in capsys.readouterr().out


def test_update_contact_supports_partial_updates(temporary_database, capsys):
    original = Namespace(
        name="Ada Lovelace",
        phone="1234567890",
        email=None,
        address=None,
        notes=None,
    )
    service.add_contact(original)
    capsys.readouterr()

    service.update_contact(Namespace(id=1, name="Augusta King"))

    record = repository.fetch_one_record(1)
    assert record["name"] == "Augusta King"
    assert record["phone"] == "1234567890"
    assert "updated successfully" in capsys.readouterr().out


def test_add_contact_reports_invalid_email_without_inserting(
    temporary_database, capsys
):
    contact = Namespace(
        name="Ada Lovelace",
        phone="1234567890",
        email="not-an-email",
        address=None,
        notes=None,
    )

    service.add_contact(contact)

    assert repository.fetch_all_records() == []
    assert "not valid input" in capsys.readouterr().out


def test_add_contact_rejects_missing_or_blank_name(temporary_database, capsys):
    for name in (None, "   "):
        service.add_contact(Namespace(
            name=name,
            phone="1234567890",
            email=None,
            address=None,
            notes=None,
        ))

    assert repository.fetch_all_records() == []
    assert capsys.readouterr().out.count("not valid input") == 2


def test_search_rejects_empty_query_and_handles_missing_phone(
    temporary_database, capsys
):
    service.add_contact(Namespace(
        name="Ada Lovelace",
        phone=None,
        email=None,
        address=None,
        notes=None,
    ))
    capsys.readouterr()

    service.search_contacts(Namespace(query=None))
    assert "non-empty search query is required" in capsys.readouterr().out

    service.search_contacts(Namespace(query="Ada"))
    assert "Ada Lovelace" in capsys.readouterr().out


def test_list_contacts_applies_limit_and_offset(temporary_database, capsys):
    for name in ("Ada Lovelace", "Grace Hopper", "Katherine Johnson"):
        service.add_contact(Namespace(
            name=name,
            phone="1234567890",
            email=None,
            address=None,
            notes=None,
        ))
    capsys.readouterr()

    service.list_contacts(Namespace(limit=1, offset=1))

    output = capsys.readouterr().out
    assert "Grace Hopper" in output
    assert "Ada Lovelace" not in output
    assert "Katherine Johnson" not in output