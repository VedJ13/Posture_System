import streamlit as st
import pandas as pd
from components.styles import apply_global_styles
from components.state import init_app_state

st.set_page_config(page_title="History", page_icon="🕘", layout="wide", initial_sidebar_state="expanded")
apply_global_styles()
init_app_state()

if not st.session_state.get("logged_in", False):
    st.warning("Please log in from the home page.")
    st.stop()

st.title("🕘 Session History")

records = st.session_state.session_records
if not records:
    st.info("Your saved sessions will appear here.")
    st.stop()

df = pd.DataFrame(records)
st.dataframe(df, use_container_width=True)

best = max(records, key=lambda r: (r["good"] / max(1, (r["good"]+r["warn"]+r["bad"]))))
worst = max(records, key=lambda r: r["bad"])
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"<div class='card'><b>Best session</b><br>{best['date']}<br>Alerts: {best['alerts']}</div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='card'><b>Highest bad posture session</b><br>{worst['date']}<br>Bad frames: {worst['bad']}</div>", unsafe_allow_html=True)
