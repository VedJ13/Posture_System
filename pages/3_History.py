import streamlit as st
import pandas as pd
from components.styles import apply_global_styles
from components.state import init_app_state

st.set_page_config(page_title="Analysis", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
apply_global_styles()
init_app_state()

if not st.session_state.get("logged_in", False):
    st.warning("Please log in from the home page.")
    st.stop()

st.title("📊 Session Analysis")

records = st.session_state.session_records
if not records:
    st.info("No completed sessions yet. Run a live session and stop it to save analysis.")
    st.stop()

df = pd.DataFrame(records)
df["total"] = df["good"] + df["warn"] + df["bad"]
df["good_pct"] = (df["good"] / df["total"] * 100).round(1)
df["bad_pct"] = (df["bad"] / df["total"] * 100).round(1)
df["duration_min"] = (df["duration_sec"] / 60).round(1)

latest = df.iloc[-1]
c1, c2, c3 = st.columns(3)
c1.metric("Latest posture score", f"{latest['good_pct']}%")
c2.metric("Latest bad posture %", f"{latest['bad_pct']}%")
c3.metric("Latest session duration", f"{latest['duration_min']} min")

st.dataframe(df[["date","duration_min","alerts","good_pct","bad_pct"]], use_container_width=True)
st.bar_chart(df.set_index("date")[["good_pct","bad_pct"]])
