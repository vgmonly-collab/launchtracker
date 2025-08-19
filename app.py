# app.py
import streamlit as st
from lib.auth import Auth

st.set_page_config(page_title="Launch Tracker", page_icon="🚀", layout="wide")

st.markdown("""
<style>
.block-container{padding-top:1rem;padding-bottom:1rem;}
[data-testid="stSidebar"] {width: 300px;}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🚀 Launch App")

# Auth
auth = Auth()
username, role = auth.login()
if not username:
    st.stop()

st.sidebar.info(f"Signed in as **{username}** · role: `{role}`")
auth.logout()

st.sidebar.markdown("---")
st.sidebar.write("Pages: use the Navigator ←")

st.title("Launch Tracker")
st.write("Use the sidebar to switch pages.")
