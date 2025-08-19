# pages/1_Tracker.py
import streamlit as st
from lib.github_db import GitHubDB, GitConfig
from lib.models import Launch
import pandas as pd

@st.cache_data(ttl=60)
def load_db():
    cfg = GitConfig(st.secrets["GITHUB_TOKEN"], st.secrets["GITHUB_REPO"], st.secrets.get("GITHUB_BRANCH","main"), st.secrets["DATA_PATH"])
    db = GitHubDB(cfg)
    return db, [Launch(**x) for x in db.read_json()]

def save_db(db, launches, message):
    db.write_json([l.model_dump() for l in launches], message)
    load_db.clear()

st.title("📋 Tracker")
role = st.session_state.get("role","viewer")
username = st.session_state.get("username","?")

with st.spinner("Loading..."):
    db, launches = load_db()

rows = []
for l in launches:
    rows.append({
        "Title": l.title,
        "Customer": l.customer,
        "Launch Month": l.launch_month,
        "Next Step": l.next_step,
        "Delayed At": l.delayed_at or "—",
        "Status": l.status,
        "ID": l.id,
    })

df = pd.DataFrame(rows)
if df.empty:
    st.warning("No launches available.")
else:
    st.dataframe(df.drop(columns=["ID"]), use_container_width=True, hide_index=True)
