import sqlite3

def log_interaction(anon_id, action, email=None):
    # 1. Connect to our database
    conn = sqlite3.connect('butterfly_tracker.db')
    cursor = conn.cursor()

    # 2. The SQL 'INSERT' command
    # We use '?' as placeholders to keep the data safe (security best practice)
    query = "INSERT INTO interactions (anon_id, action, email) VALUES (?, ?, ?)"
    
    # 3. Execute and Save
    cursor.execute(query, (anon_id, action, email))
    conn.commit()
    conn.close()
    print(f"Action Logged: {anon_id} performed '{action}'")

# --- SIMULATE A STRANGER (Butterfly) ---
# Imagine a visitor arrives with a temporary ID 'cookie_777'
print("--- User starts browsing anonymously ---")
log_interaction('cookie_777', 'visited_homepage')
log_interaction('cookie_777', 'viewed_luxury_watch')
log_interaction('cookie_777', 'added_to_cart')

print("\nSuccess! Open 'DB Browser for SQLite' to see your data.")