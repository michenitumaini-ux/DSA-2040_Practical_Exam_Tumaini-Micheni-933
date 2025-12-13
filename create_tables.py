import sqlite3

def create_tables(db_name='retail_dw.db'):
    """
    Creates the retail data warehouse tables in SQLite.
    """
    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # ------------------- CustomerDim -------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS CustomerDim (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cust_raw_id INTEGER,
        name TEXT,
        gender TEXT,
        age INTEGER,
        country TEXT,
        city TEXT,
        segment TEXT
    );
    """)

    # ------------------- ProductDim -------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ProductDim (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_code TEXT,
        product_name TEXT,
        category TEXT,
        brand TEXT,
        unit_price REAL
    );
    """)

    # ------------------- TimeDim -------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS TimeDim (
        time_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        day INTEGER,
        month INTEGER,
        quarter INTEGER,
        year INTEGER,
        is_weekend INTEGER
    );
    """)

    # ------------------- SalesFact -------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS SalesFact (
        sales_id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_no TEXT,
        product_id INTEGER,
        customer_id INTEGER,
        time_id INTEGER,
        quantity INTEGER,
        unit_price REAL,
        sales_amount REAL,
        country TEXT,
        FOREIGN KEY(product_id) REFERENCES ProductDim(product_id),
        FOREIGN KEY(customer_id) REFERENCES CustomerDim(customer_id),
        FOREIGN KEY(time_id) REFERENCES TimeDim(time_id)
    );
    """)

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print(f"Database '{db_name}' created and tables initialized successfully!")

# ------------------- Main -------------------
if __name__ == "__main__":
    create_tables()
