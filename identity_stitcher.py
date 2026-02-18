import sqlite3

def stitch_identity(anon_id, user_email):
    # 1. Connect to our database
    conn = sqlite3.connect('butterfly_tracker.db')
    cursor = conn.cursor()

    print(f"--- Identity Found: {user_email} ---")
    
    # 2. THE STITCH: Update all old rows where the email was empty
    # This is the "Identity Resolution" logic
    stitch_query = """
    UPDATE interactions 
    SET email = ? 
    WHERE anon_id = ? AND email IS NULL
    """
    
    cursor.execute(stitch_query, (user_email, anon_id))
    
    # 3. Check how many 'Butterfly' actions we just linked
    rows_affected = cursor.rowcount
    conn.commit()
    
    print(f"Successfully stitched {rows_affected} anonymous actions to {user_email}!")

    # 4. THE SNIPER TRIGGER: If they have more than 2 luxury views, alert the team
    cursor.execute("SELECT COUNT(*) FROM interactions WHERE email = ?", (user_email,))
    total_actions = cursor.fetchone()[0]
    
    if total_actions >= 3:
        print(f"!!! SNIPER ALERT !!!")
        print(f"Target {user_email} has reached {total_actions} interactions.")
        print("Sending a 15% Precision Discount Coupon now...")

    conn.close()

# --- SIMULATE THE USER LOGGING IN ---
# Our stranger 'cookie_777' finally signs up with an email!
stitch_identity('cookie_777', 'liwu_fan@example.com')