import streamlit as st
import requests
import pandas as pd
import sqlite3
import time

# The address of your FastAPI server
BASE_URL = "http://127.0.0.1:8000"

st.title("🦋 The Butterfly Tracker")
st.subheader("Simulate User Interactions")

# 1. Input for Anonymous ID
anon_id = st.text_input("Device ID (Cookie)", value="cookie_999")

# 2. Buttons to simulate 'Actions'
st.write("Click a button to perform an action:")
col1, col2, col3 = st.columns(3)

if col1.button("View Product"):
    res = requests.post(f"{BASE_URL}/capture", json={"anon_id": anon_id, "action": "view_product"})
    st.success("Action Logged!")

if col2.button("Add to Cart"):
    res = requests.post(f"{BASE_URL}/capture", json={"anon_id": anon_id, "action": "add_to_cart"})
    st.success("Action Logged!")

# 3. The 'Stitch' Area (Login)
st.divider()
st.subheader("👤 Create a Bond (Login)")
email = st.text_input("Enter Email to Login")

if st.button("Log In & Stitch"):
    if email:
        # This calls the 'stitch' endpoint we made in server.py
        res = requests.post(f"{BASE_URL}/stitch?anon_id={anon_id}&email={email}")
        data = res.json()
        st.write(f"Status: {data['status']}")
        st.info(f"Bonded {data['interactions_found']} past actions to {email}")
    else:
        st.warning("Please enter an email!")

st.divider()
st.subheader("📊 Live Sniper Feed")

# 1. This function reads the database and turns it into a table
def get_live_data():
    conn = sqlite3.connect('butterfly_tracker.db')
    # We use Pandas to read the SQL table easily
    df = pd.read_sql_query("SELECT * FROM interactions ORDER BY id DESC LIMIT 10", conn)
    conn.close()
    return df

# 2. This is the "Magic" part: A fragment that runs every 2 seconds
@st.fragment(run_every=2)
def show_live_table():
    data = get_live_data()
    # Display the data as a nice interactive table
    st.dataframe(data, width="stretch")

    # Add a checkbox at the top or bottom
    show_stats = st.checkbox("Show Sniper Analytics")

    if show_stats:
        st.subheader("📈 Interaction Breakdown")
        status_counts = data['email'].isna().value_counts()
        status_counts.index = status_counts.index.map({True: 'Butterflies🦋', False: 'Identified✅'})
        st.bar_chart(status_counts, horizontal=True, x_label="Total Actions", y_label="Status")

# 3. Call the fragment
show_live_table()