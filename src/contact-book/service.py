# Implementation of code logic.
from pydantic import ValidationError
import repository
from validators import ContactModel

def add_contact(Contact:ContactModel):
    try:

        Contact = ContactModel(**vars(Contact))

        contact_id = repository.insert_record(Contact)
        print(f"Contact inserted successfully! assigned id {contact_id}")
        
    except ValidationError as e:
        errors_list = e.errors()

        for error in errors_list:
            print(f"'{error['input']}' is not valid input! {error['msg']}.")


def list_contacts(Contact):
    
    records = repository.fetch_all_records()

    if records:
        for record in records:
            print_contact(record)
    else:
        print(f"There are no contacts saved.")


def search_contacts(Contact):
    records = repository.fetch_all_records()

    result = []

    for record in records:
        if Contact.query in record['name'] or Contact.query in record['phone']:
            result.append(record)

    if result:
        for contact in result:
            print_contact(contact)
    else:
        print("No results found!")


def update_contact(Contact):

    try:
        Contact = ContactModel(**vars(Contact))
        Contact = vars(Contact)

        set_clause = {key:value for key, value in Contact.items() if value is not None and key not in ('id', 'func', 'command')}
        

        data = [value for value in set_clause.values()]
        data.append(Contact['id'])
        data = tuple(data)
        print(data)

        set_clause = [f'{key} = ?,' for key in set_clause.keys()]
        set_clause_str = ''

        for value in set_clause:
            set_clause_str += value

        set_clause_str = set_clause_str.strip(',')
        print(set_clause_str)

        update_successful = repository.update_record(set_clause_str, data)

        if update_successful:
            print(f"Contact with id {Contact['id']} updated successfully!")


    except ValidationError as e:
        errors_list = e.errors()

        for error in errors_list:
            print(f"'{error['input']}' is not valid input! {error['msg']}.")


def show_command(Contact):

    contact = repository.fetch_one_record(Contact.id)
    if contact:
        print_contact(contact)
    else:
        print(f"There is no any contact with id {Contact.id}.")


def delete_contact(Contact):

    deleted_successfully = repository.delete_record(Contact.id)

    if deleted_successfully:
        print(f"Contact with {Contact.id} deleted successfully!")
    else:
        print(f"There is no any contact with id {Contact.id}.")


def count_contacts(Contact):

    count = repository.count_records(args)[0][0]

    print(f"There are total {count} contacts!")


def print_contact(Contact):

    contact = dict(Contact)

    print('-' * 70)
    print(f'{'DETAILS':>38}')
    print('-' * 70)

    contact = {key:(f'None' if val is None else val) for key, val in contact.items()}

    print(f'{'ID':^35} | {contact['id']:^35}')
    print(f'{'NAME':^35} | {contact['name']:^35}')
    print(f'{'PHONE':^35} | {contact['phone']:^35}')
    print(f'{'EMAIL':^35} | {contact['email']:^35}')
    print(f'{'ADDRESS':^35} | {contact['address']:^35}')
    print(f'{'NOTES':^35} | {contact['notes']:^35}')
    print(f'{'CREATED_AT':^35} | {contact['created_at']:^35}')
    print(f'{'UPDATED_AT':^35} | {contact['updated_at']:^35}')