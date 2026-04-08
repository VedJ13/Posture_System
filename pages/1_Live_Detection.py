import time
import streamlit as st
from streamlit_webrtc import webrtc_streamer
from components.styles import apply_global_styles
from components.state import init_app_state, get_shared_state, apply_thresholds, reset_live_flags
from components.detector import PostureProcessor
from collections import deque

st.set_page_config(page_title="Live Detection", page_icon="🧘", layout="wide", initial_sidebar_state="expanded")
apply_global_styles()
init_app_state()
apply_thresholds()
shared = get_shared_state()

if not st.session_state.get("logged_in", False):
    st.warning("Please log in from the home page.")
    st.stop()

with st.sidebar:
    st.markdown("## Controls")
    st.select_slider("Shoulder tilt sensitivity", ["Low", "Medium", "High"], key="sensitivity")
    st.slider("Alert cooldown (sec)", 5, 60, key="alert_cooldown")
    st.toggle("Voice alerts", key="voice_alerts")
    st.toggle("Red overlay", key="red_overlay_on")
    if st.button("Reset detector state", use_container_width=True):
        reset_live_flags()
        st.rerun()

apply_thresholds()

st.title("🧘 Live Detection")
st.caption("Start the camera widget first, then begin your session.")

with shared["lock"]:
    posture_now = shared["posture"]
    camera_on = shared["camera_on"]
    last_diff = shared["last_diff"]

if st.session_state.session_active and posture_now not in ("Waiting…", "No Pose"):
    now = time.time()
    if posture_now == "Good Posture":
        st.session_state.total_good += 1
    elif posture_now == "Slightly Bent":
        st.session_state.total_warn += 1
    elif posture_now == "Bad Posture":
        st.session_state.total_bad += 1
        if now - st.session_state.last_alert_time >= st.session_state.alert_cooldown:
            st.session_state.last_alert_time = now
            st.session_state.alert_count += 1
    st.session_state.history.append({"t": now, "posture": posture_now, "diff": last_diff})

c1, c2 = st.columns([3,2])

with c1:
    b1, b2 = st.columns(2)
    with b1:
        if st.button("▶ Start Session", use_container_width=True, type="primary", disabled=not camera_on):
            st.session_state.session_active = True
            st.session_state.session_start = time.time()
            st.session_state.total_good = 0
            st.session_state.total_warn = 0
            st.session_state.total_bad = 0
            st.session_state.alert_count = 0
            st.session_state.last_alert_time = 0.0
            st.session_state.history = deque(maxlen=240)
            st.rerun()
    with b2:
        if st.button("⏹ Stop Session", use_container_width=True, disabled=not st.session_state.session_active):
            total = st.session_state.total_good + st.session_state.total_warn + st.session_state.total_bad
            if total > 0 and st.session_state.session_start:
                duration = int(time.time() - st.session_state.session_start)
                record = {
                    "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "duration_sec": duration,
                    "good": st.session_state.total_good,
                    "warn": st.session_state.total_warn,
                    "bad": st.session_state.total_bad,
                    "alerts": st.session_state.alert_count,
                }
                st.session_state.session_records.append(record)
            st.session_state.session_active = False
            reset_live_flags()
            st.rerun()

    if not camera_on:
        st.markdown("<div class='warn-banner'>📷 Click <b>START</b> in the camera widget below, allow camera access, then press ▶ Start Session above.</div>", unsafe_allow_html=True)

    webrtc_streamer(
        key="posture",
        video_processor_factory=PostureProcessor,
        rtc_configuration={
            "iceServers": [
                {"urls": ["stun:stun.l.google.com:19302"]},
                {"urls": ["stun:stun1.l.google.com:19302"]},
                {"urls": ["turn:openrelay.metered.ca:80"], "username": "openrelayproject", "credential": "openrelayproject"},
            ]
        },
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

    if st.session_state.voice_alerts and st.session_state.alert_count > 0:
        st.components.v1.html(f"""
        <script>
        const k = "{st.session_state.alert_count}";
        window.parent.__ps_last = window.parent.__ps_last || "0";
        if (k !== "0" && window.parent.__ps_last !== k) {{
            window.parent.__ps_last = k;
            const u = new SpeechSynthesisUtterance("Bad posture detected. Please sit up straight.");
            window.parent.speechSynthesis.cancel();
            window.parent.speechSynthesis.speak(u);
        }}
        </script>
        """, height=0)

with c2:
    total = st.session_state.total_good + st.session_state.total_warn + st.session_state.total_bad
    gp = round(st.session_state.total_good / total * 100) if total else 0
    wp = round(st.session_state.total_warn / total * 100) if total else 0
    bp = round(st.session_state.total_bad / total * 100) if total else 0
    pill = {"Good Posture":"pg","Slightly Bent":"pw","Bad Posture":"pb"}.get(posture_now, "pi")
    st.markdown(f"<span class='pill {pill}'>{posture_now}</span>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Alerts</div><div class='metric-value bad'>{st.session_state.alert_count}</div></div>", unsafe_allow_html=True)
    with m2:
        elapsed = "--:--"
        if st.session_state.session_start:
            sec = int(time.time() - st.session_state.session_start)
            elapsed = f"{sec//60:02d}:{sec%60:02d}"
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Session Time</div><div class='metric-value'>{elapsed}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='card'>Shoulder difference: <b>{last_diff:.4f}</b><br>Good: <b>{gp}%</b> · Warn: <b>{wp}%</b> · Bad: <b>{bp}%</b></div>", unsafe_allow_html=True)

@st.fragment(run_every=1)
def _tick():
    st.caption("Live stats refresh every second while this page is open.")

_tick()
