# Implementation of code logic.
from pydantic import ValidationError
import repository
from validators import ContactModel
from datetime import datetime

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
        
        print('-' * 113)
        print('-' * 113)

        print(f"|| {'ID':<5} || {'NAME':30} || {'PHONE':<30} || {'EMAIL':<30} ||")
        print('-' * 113)

        for record in records:
            record = dict(record)
            record = {key:(f'None' if val is None else val) for key, val in record.items()}
            print(f'|| {record['id']:<5} || {record['name']:<30} || {record['phone']:<30} || {record['email']:<30} ||')

        print('-' * 113)
        print('-' * 113)
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
        

        data = (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),*[value for value in set_clause.values()],Contact['id'])

        # data.append(Contact['id'])
        data = tuple(data)
        print(data)

        set_clause = [f'{key} = ?,' for key in set_clause.keys()]
        set_clause_str = 'updated_at = ?, '

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

    print('-' * 100)
    print('-' * 100)

    contact = {key:(f'None' if val is None else val) for key, val in contact.items()}

    print(f'|| {'ID':<11} || {contact['id']:<79} ||')
    print(f'|| {'NAME':<11} || {contact['name']:<79} ||')
    print(f'|| {'PHONE':<11} || {contact['phone']:<79} ||')
    print(f'|| {'EMAIL':<11} || {contact['email']:<79} ||')
    print(f'|| {'ADDRESS':<11} || {contact['address']:<79} ||')
    print(f'|| {'NOTES':<11} || {contact['notes']:<79} ||')
    print(f'|| {'CREATED_AT':<11} || {contact['created_at']:<79} ||')
    print(f'|| {'UPDATED_AT':<11} || {contact['updated_at']:<79} ||')

    print('-' * 100)
    print('-' * 100)