import sqlite3

try:
    conn = sqlite3.connect("backend/app.db", timeout=10)
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE datasets ADD COLUMN date_col VARCHAR")
    cursor.execute("ALTER TABLE datasets ADD COLUMN category_col VARCHAR")
    cursor.execute("ALTER TABLE datasets ADD COLUMN value_col VARCHAR")
    cursor.execute("ALTER TABLE datasets ADD COLUMN is_cleaned BOOLEAN DEFAULT 0")
    cursor.execute("ALTER TABLE datasets ADD COLUMN cleaned_file_path VARCHAR")
    conn.commit()
    print("Database updated successfully.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("Columns already exist.")
    else:
        print("Error:", e)
finally:
    conn.close()
