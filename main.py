import sqlite3
from pathlib import Path
from typing import Optional

def connect_db(db: str):
    parent = Path(__file__).parent
    dir = parent / "db"
    file = dir / db

    dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(file)
    print("Connected to the database successfully!")
    return conn

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS anidb (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        cover TEXT,
        status INTEGER NOT NULL CHECK(status IN (1, 2, 3))
    )
    ''')
    conn.commit()

def insert_data(conn, title: str, cover: Optional[str], status: int):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO anidb (title, cover, status) VALUES (?, ?, ?)
    ''', (title, cover, status))
    conn.commit()
    print("Anime added successfully!")

def query_data(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM anidb')
    rows = cursor.fetchall()
    
    if rows:
        for row in rows:
            print(row)
    else:
        print("No anime found in the database.")

def delete_data(conn, anime_id: int):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM anidb WHERE id = ?', (anime_id,))
    conn.commit()
    if cursor.rowcount > 0:
        print(f"Anime with ID {anime_id} deleted successfully!")
    else:
        print(f"No anime found with ID {anime_id}.")

def dialog(conn):
    print("Welcome to anidb! What do you want to do?")

    options = [
        "1. Get your anime list",
        "2. Insert new anime to the list",
        "3. Delete an anime from the list"
    ]

    for o in options:
        print(o)
    
    choice = input("Choose an option from the above: ")
    
    if choice == "1":
        query_data(conn)
    elif choice == "2":
        name = input("Anime title: ").strip()
        cover = input("Anime cover (url) [Press enter to skip]: ").strip() or None
        status = input("Anime status (1 for releasing, 2 for completed, 3 for not yet released): ")
        try:
            status = int(status)
            if status not in [1, 2, 3]:
                raise ValueError
            insert_data(conn, name, cover, status)
        except ValueError:
            print("Invalid input. Please ensure the status is 1, 2, or 3.")
    elif choice == "3":
        try:
            anime_id = int(input("Enter the ID of the anime to delete: "))
            delete_data(conn, anime_id)
        except ValueError:
            print("Invalid ID input. Please enter a numeric ID.")
    else:
        print("Oops! The only available options are 1 & 2.")

def main():
    conn = connect_db("database.db")
    create_table(conn)
    dialog(conn)
    conn.close()

if __name__ == "__main__":
    main()