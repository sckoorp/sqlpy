import sqlite3
from pathlib import Path
from typing import Optional

def connect_db(db: str):
    parent = Path(__file__).parent
    dir = parent / "db"
    file = dir / db

    if not dir.exists():
        dir.mkdir(parents=True, exist_ok=True)
    
    if not file.exists():
        with sqlite3.connect(file) as conn:
            print("Initialized database successfully!")
    else:
        conn = sqlite3.connect(file)
            
    return conn
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS anidb (
        id INTEGER NOT NULL UNIQUE,
        title TEXT NOT NULL,
        cover INTEGER,
        status INTEGER NOT NULL CHECK(status IN (1, 3)),
        PRIMARY KEY(id AUTOINCREMENT)
    )
    ''')
    conn.commit()

def insert_data(conn, title: str, cover: Optional[str], status: int):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO anidb (title, cover, status) VALUES (?, ?, ?)
    ''', (title, cover, status))
    conn.commit()

def query_data(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM anidb')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def dialog(conn):
    print("Welcome to anidb! What do you want to do?")

    options = ["1. Get your anime list", "2. Insert new anime to the list"]
    for o in options:
        print(o)
    
    choice = input("Choose an option from the above: ")
    
    if choice == "1":
        query_data(conn)
    elif choice == "2":
        name = input("Anime title: ")
        cover = input("Anime cover (url): ")
        status = input("Anime status (1 for releasing, 2 for completed, 3 for not yet released): ")
        try:
            status = int(status)
            insert_data(conn, name, cover if cover else None, status)
        except ValueError:
            print("Invalid status input. Please enter 1 or 3.")
    else:
        print("Oops! The only available options are 1 & 2.")

def main():
    conn = connect_db("database.db")
    create_table(conn)
    dialog(conn)
    conn.close()

if __name__ == "__main__":
    main()