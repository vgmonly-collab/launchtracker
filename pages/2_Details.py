# pages/2_Details.py
import streamlit as st
from lib.github_db import GitHubDB, GitConfig
from lib.models import Launch

@st.cache_data(ttl=60)
def load_db():
    cfg = GitConfig(st.secrets["GITHUB_TOKEN"], st.secrets["GITHUB_REPO"], st.secrets.get("GITHUB_BRANCH","main"), st.secrets["DATA_PATH"])
    db = GitHubDB(cfg)
    return db, [Launch(**x) for x in db.read_json()]

st.title("🔎 Details")
sel = st.session_state.get("detail_id")
if not sel:
    st.info("Open Details from the Tracker page.")
    st.stop()

_, launches = load_db()
match = [l for l in launches if l.id == sel]
if not match:
    st.error("Launch not found.")
    st.stop()

l = match[0]

st.subheader(l.title)
st.write(f"**Customer:** {l.customer}")
st.write(f"**Launch Month:** {l.launch_month}")
st.write(f"**Next Step:** {l.next_step}")
st.write(f"**Delayed At:** {l.delayed_at or '—'}")
st.write(f"**Status:** {l.status}")
