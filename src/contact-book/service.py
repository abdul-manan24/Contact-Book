# Implementation of code logic.
import repository

def add_contact(Contact):
    
    contact_id = repository.insert_record(Contact)
    print(f"Contact inserted successfully! assigned id {contact_id}")

def list_contacts():
    pass

def search_contacts():
    pass

def update_contact(Contact):
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

    repository.update_record(set_clause_str, data)

    print(f"Contact with id {Contact['id']} updated successfully!")

def show_command(Contact):

    contact = dict(repository.fetch_one_record(Contact.id))

    print(type(contact))
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




def delete_contact(Contact):
    repository.delete_record(Contact.id)
    print(f"Contact with {Contact.id} deleted successfully!")

def count_contacts(args):

    count = repository.count_records(args)[0][0]

    print(f"There are total {count} contacts!")