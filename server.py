import os
from dotenv import load_dotenv
import requests
from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development, allow everything
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# 1. Define what an "Action" looks like (a Pydantic model)
class Interaction(BaseModel):
    anon_id: str
    action: str
    email: str = None

def send_sniper_alert(email, count):
    message = {
        "content": f"🎯 **SNIPER ALERT!**\nUser **{email}** has completed the Bond with **{count}** interactions. Sending precision offer!"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=message)
    # Check for the DISCORD ERROR:
    print(f"Discord Response: {response.status_code} - {response.text}")


# --- THE ALL-IN-ONE BRAIN ---
@app.post("/capture")
def capture_action(item: Interaction):
    conn = sqlite3.connect('butterfly_tracker.db')
    cursor = conn.cursor()

    # 1. Retroactive Stitch: If a new email just arrived, update the past
    if item.email:
        cursor.execute("UPDATE interactions SET email = ? WHERE anon_id = ? AND email IS NULL", (item.email, item.anon_id))
    
    # 2. Recognition: Check if this anon_id was bonded in a PREVIOUS request
    current_email = item.email
    if not current_email:
        cursor.execute("SELECT email FROM interactions WHERE anon_id = ? AND email IS NOT NULL LIMIT 1", (item.anon_id,))
        result = cursor.fetchone()
        if result:
            current_email = result[0]

    # 3. Record the current action
    cursor.execute("INSERT INTO interactions (anon_id, action, email) VALUES (?, ?, ?)", 
                   (item.anon_id, item.action, current_email))
    conn.commit()

    # 4. Trigger Alerts
    if current_email:
        cursor.execute("SELECT COUNT(*) FROM interactions WHERE email = ?", (current_email,))
        count = cursor.fetchone()[0]
        # Alert on the 3rd, 6th, 9th interaction...
        if count > 0 and count % 3 == 0:
            send_sniper_alert(current_email, count)

    conn.close()
    return {"status": "success", "identified_as": current_email}


"""@app.post("/stitch")
def stitch_user(anon_id: str, email: str):
    conn = sqlite3.connect('butterfly_tracker.db')
    cursor = conn.cursor()
    
    # 1. Perform the Stitch
    cursor.execute("UPDATE interactions SET email = ? WHERE anon_id = ? AND email IS NULL", (email, anon_id))
    
    # 2. Check total interactions for this Bond
    cursor.execute("SELECT COUNT(*) FROM interactions WHERE email = ?", (email,))
    count = cursor.fetchone()[0]
    conn.commit()
    conn.close()

    # 3. Trigger the Sniper Alert if they are active enough
    if count >= 3:
        send_sniper_alert(email, count)
        
    return {"status": "bonded", "user": email, "interactions_found": count}
"""

"""
@app.post("/capture")
async def capture_action(data: Interaction):
    conn = sqlite3.connect('bond_engine.db')
    cursor = conn.cursor()
    
    # 1. Save the current action
    cursor.execute(
        "INSERT INTO observations (anon_id, action, email) VALUES (?, ?, ?)",
        (data.anon_id, data.action, data.email)
    )
    
    # 2. THE STITCH: If an email is present, update ALL past actions for this ID
    if data.email:
        cursor.execute(
            "UPDATE observations SET email = ? WHERE anon_id = ?",
            (data.email, data.anon_id)
        )
    
    conn.commit()
    conn.close()
    return {"status": "Identity Bonded" if data.email else "Action Tracked"}

"""



"""# 3. The "Stitch" Endpoint (The Bond Creator)
@app.post("/stitch")
def stitch_user(anon_id: str, email: str):
    conn = sqlite3.connect('butterfly_tracker.db')
    cursor = conn.cursor()

    # Use .strip() to remove accidental spaces in the ID or Email
    anon_id = anon_id.strip()
    email = email.strip()

    cursor.execute(
        "UPDATE interactions SET email = ? WHERE anon_id = ? AND email IS NULL",
        (email, anon_id)
    )
    conn.commit()
    conn.close()
    return {"status": "bonded", "user": email}  
"""
"""
@app.post("/capture")
def capture_action(item: Interaction):
    conn = sqlite3.connect('butterfly_tracker.db')
    cursor = conn.cursor()

    # 1. NEW LOGIC: Check if this anon_id already belongs to a known email
    cursor.execute("SELECT email FROM interactions WHERE anon_id = ? AND email IS NOT NULL LIMIT 1", (item.anon_id,))
    existing_bond = cursor.fetchone()

    # 2. If we found a bond, use that email!
    assigned_email = item.email # Start with what was sent (usually None)
    if existing_bond:
        assigned_email = existing_bond[0]
        print(f"Target Recognized! Linking action to {assigned_email}")

    # 3. Save the interaction with the auto-filled email
    cursor.execute(
        "INSERT INTO interactions (anon_id, action, email) VALUES (?, ?, ?)",
        (item.anon_id, item.action, assigned_email)
    )
    
    conn.commit()
    conn.close()
    return {"status": "success", "identified_as": assigned_email}"""