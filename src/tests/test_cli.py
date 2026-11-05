import sys
import pytest
from unittest.mock import MagicMock, patch

# Assuming your original code is in a file named cli.py
from contact_book.cli import build_parser, service


@pytest.fixture
def parser():
    """Provides a fresh parser instance for each test."""
    return build_parser()


# --- SUCCESS CASES ---

def test_add_command(parser):
    """Tests that the 'add' subcommand parses all fields correctly."""
    test_args = [
        "Contact", "add", 
        "--name", "John Doe", 
        "--phone", "12345", 
        "--email", "john@example.com", 
        "--address", "123 St", 
        "--notes", "Friend"
    ]
    with patch.object(sys, 'argv', test_args):
        args = parser.parse_args()
        assert args.command == "add"
        assert args.name == "John Doe"
        assert args.phone == "12345"
        assert args.email == "john@example.com"
        assert args.address == "123 St"
        assert args.notes == "Friend"
        assert args.func == service.add_contact


def test_list_command_defaults(parser):
    """Tests that 'list' applies correct defaults when flags are missing."""
    test_args = ["Contact", "list"]
    with patch.object(sys, 'argv', test_args):
        args = parser.parse_args()
        assert args.command == "list"
        assert args.limit == 20
        assert args.offset == 0
        assert args.func == service.list_contacts


def test_list_command_custom_values(parser):
    """Tests that 'list' properly overrides limits and offsets."""
    test_args = ["Contact", "list", "--limit", "50", "--offset", "10"]
    with patch.object(sys, 'argv', test_args):
        args = parser.parse_args()
        assert args.limit == 50
        assert args.offset == 10


def test_search_command(parser):
    """Tests 'search' with query string and limits."""
    test_args = ["Contact", "search", "--query", "Alice", "--limit", "10"]
    with patch.object(sys, 'argv', test_args):
        args = parser.parse_args()
        assert args.command == "search"
        assert args.query == "Alice"
        assert args.limit == 10


def test_show_command(parser):
    """Tests 'show' converts ID to an integer."""
    test_args = ["Contact", "show", "--id", "5"]
    with patch.object(sys, 'argv', test_args):
        args = parser.parse_args()
        assert args.command == "show"
        assert args.id == 5


def test_update_command(parser):
    """Tests 'update' handles partial field edits alongside ID."""
    test_args = ["Contact", "update", "--id", "42", "--name", "Jane"]
    with patch.object(sys, 'argv', test_args):
        args = parser.parse_args()
        assert args.command == "update"
        assert args.id == 42
        assert args.name == "Jane"
        assert args.email is None  # Other fields remain unassigned


def test_delete_command_with_confirmation_skip(parser):
    """Tests 'delete' handles flag actions like --yes."""
    test_args = ["Contact", "delete", "--id", "12", "--yes"]
    with patch.object(sys, 'argv', test_args):
        args = parser.parse_args()
        assert args.command == "delete"
        assert args.id == 12
        assert args.yes is True


def test_count_command(parser):
    """Tests the basic 'count' route functionality."""
    test_args = ["Contact", "count"]
    with patch.object(sys, 'argv', test_args):
        args = parser.parse_args()
        assert args.command == "count"
        assert args.func == service.count_contacts


# --- ERROR & VALIDATION CASES ---

def test_missing_command_raises_error(parser):
    """Tests that omitting a command entirely triggers SystemExit."""
    test_args = ["Contact"]
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit):
            parser.parse_args()


def test_invalid_type_raises_error(parser):
    """Tests that passing text into an integer field flags an error."""
    test_args = ["Contact", "show", "--id", "not-a-number"]
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit):
            parser.parse_args()
