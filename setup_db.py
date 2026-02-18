import sqlite3

# 1. Connect to (or create) the database file
# This creates a file named 'butterfly_tracker.db' in your folder
connection = sqlite3.connect('butterfly_tracker.db')
cursor = connection.cursor()

# 2. Create the 'interactions' table
# This is where we store every 'click' or 'view'
cursor.execute('''
CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    anon_id TEXT,        -- A temporary ID for a stranger
    email TEXT,          -- This stays NULL until the 'Stitch' happens
    action TEXT,         -- What did they do? (e.g., 'view_product')
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# 3. Save (commit) and close
connection.commit()
connection.close()

print("Success: Your 'Butterfly' database is ready!")