import sqlite3


class Database:
    """Handles the SQLite connection and table creation."""

    def __init__(self, db_name="pos.db"):
        self.connection = sqlite3.connect(db_name)
        self.connection.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        self.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                price REAL NOT NULL,
                stock INTEGER NOT NULL
            )
        """)
        self.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                total REAL NOT NULL,
                payment_method TEXT NOT NULL,
                amount_paid REAL NOT NULL,
                change_due REAL NOT NULL
            )
        """)
        self.execute("""
            CREATE TABLE IF NOT EXISTS transaction_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (transaction_id) REFERENCES transactions (id)
            )
        """)

    def execute(self, query, params=()):
        cursor = self.connection.execute(query, params)
        self.connection.commit()
        return cursor

    def fetch_all(self, query, params=()):
        return self.connection.execute(query, params).fetchall()

    def fetch_one(self, query, params=()):
        return self.connection.execute(query, params).fetchone()

    def close(self):
        self.connection.close()