# It contains raw SQL queries.
import sqlite3
from db import connect
from models import Contact
from datetime import datetime

def insert_record(Contact: Contact) -> int:
    with connect() as conn:
        data = (
            Contact.name,
            Contact.phone,
            Contact.email,
            Contact.address,
            Contact.notes,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        cursor = conn.execute(
            """ INSERT INTO contacts (
            name,
            phone,
            email,
            address,
            notes,
            created_at,
            updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            data
        )

        conn.commit()
        return cursor.lastrowid


def fetch_all_records():
    with connect() as conn:
        cursor = conn.execute(
            '''SELECT * FROM contacts'''
        )

        all_records = cursor.fetchall()

        return all_records


def fetch_one_record(id: int):
    
    with connect() as conn:
        cursor = conn.execute (
            ''' SELECT * FROM contacts
                WHERE id = ?
            ''',
            (id,)
        )

        return cursor.fetchone()
    

def delete_record(id: int):
    with connect() as conn:
        cursor = conn.execute(
            ''' DELETE FROM contacts
                WHERE id = ?
            ''',
            (id,)
        )

        conn.commit()

        return cursor.rowcount


def update_record(set_clause: str, data: tuple):
    try:
        with connect() as conn:
            cursor = conn.execute(
                f''' UPDATE contacts SET {set_clause} WHERE id = ?''',
                data
            )

            conn.commit()

        return True
    
    except sqlite3.IntegrityError as e:
        print("Error occurred", e)


def count_records(args):
    
    with connect() as conn:
        cursor = conn.execute(
            ''' SELECT COUNT(*) FROM contacts'''
        )

        count = cursor.fetchall()

        return count