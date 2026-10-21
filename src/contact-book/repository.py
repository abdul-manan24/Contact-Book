# It contains raw SQL queries.
from db import connect
from models import Contact
from datetime import datetime

def add_contact(Contact) -> Contact:
    with connect() as conn:
        insert_query = '''
          INSERT INTO contacts (id, name, phone, email, address, notes, created_at, updated_at)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?)  
         '''

        data = (
            1,
            Contact.name,
            Contact.phone,
            Contact.email,
            Contact.address,
            Contact.notes,
            datetime.now(),
            datetime.now()
        )

        cursor = conn.execute(insert_query, data)

        print(f"Contact saved successfully assigned id {cursor.lastrowid}")



def list_contacts():
    pass

def search_contacts():
    pass

def show_command():
    pass

def update_contact():
    pass

def delete_contact():
    pass

def count_contacts():
    pass