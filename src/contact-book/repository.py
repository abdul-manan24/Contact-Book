# It contains raw SQL queries.
from db import connect
from models import Contact
from datetime import datetime

def add_contact(Contact) -> Contact:
    with connect() as conn:
        insert_query = '''
          INSERT INTO contacts (name, phone, email, address, notes, created_at, updated_at)
          VALUES (?, ?, ?, ?, ?, ?, ?)  
         '''

        data = (
            Contact.name,
            Contact.phone,
            Contact.email,
            Contact.address,
            Contact.notes,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        cursor = conn.execute(insert_query, data)

        print(f"Contact saved successfully assigned id {cursor.lastrowid}")



def list_contacts(limit:int = 20):
    with connect() as conn:
        cursor = conn.execute(
            ''' SELECT * FROM contacts'''
        )

        contacts = cursor.fetchall()

        HEADER = "\033[1;36m"  # Bold Cyan
        VALUE = "\033[0m"      # Normal White/Reset
        MISSING = "\033[31m"    # Red (for missing/None values)
        RESET = "\033[0m"

        print()
        print('-' * 131)
        print(f'{HEADER}{'ID':<2} | {'Name':<12} | {'Phone':<12} | {'Email':<10} | {'Address':<15} | {'Notes':<20} | {'Created_at':<20} | {'Updated_at':<20}{RESET}')
        print('-' * 131)

        for contact in contacts:
            contact = dict(contact)
            contact = {key: (f'None' if value is None else value) for key, value in contact.items()}
            print(f'{VALUE}{contact['id']:<2} | {contact['name']:<12} | {contact['phone']:<12} | {contact['email']:<10} | {contact['address']:<15} | {contact['notes']:20} | {contact['created_at']:<20} | {contact['updated_at']:<20}{RESET}')
        else:
            print('-' * 131, '\n')

def search_contacts():
    pass

def show_command():
    pass

def update_contact():
    pass

def delete_contact(args):

    contact_id = args.id

    with connect() as conn:

        cursor = conn.execute(
            ''' DELETE FROM contacts
                WHERE id = ? 
            ''',
            (contact_id,)
        )

        conn.commit()

        print(f'Contact with id -> {contact_id} deleted successfully!')

def count_contacts():
    pass