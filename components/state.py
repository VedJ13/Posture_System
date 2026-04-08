import streamlit as st
import threading
from collections import deque

_THRESH_MAP = {
    "Low": (0.13, 0.10),
    "Medium": (0.10, 0.075),
    "High": (0.07, 0.05),
}

@st.cache_resource
def get_shared_state():
    return {
        "posture": "Waiting…",
        "camera_on": False,
        "bad_thresh": 0.10,
        "warn_thresh": 0.075,
        "last_diff": 0.0,
        "lock": threading.Lock(),
    }

def init_app_state():
    defaults = dict(
        session_start=None,
        session_active=False,
        total_good=0,
        total_warn=0,
        total_bad=0,
        alert_count=0,
        last_alert_time=0.0,
        history=deque(maxlen=240),
        session_records=[],
        sensitivity="Medium",
        alert_cooldown=15,
        voice_alerts=True,
        red_overlay_on=True,
    )

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def apply_thresholds():
    shared = get_shared_state()
    bad_t, warn_t = _THRESH_MAP[st.session_state.sensitivity]

    with shared["lock"]:
        shared["bad_thresh"] = bad_t
        shared["warn_thresh"] = warn_t


def reset_live_flags():
    shared = get_shared_state()

    with shared["lock"]:
        shared["camera_on"] = False
        shared["posture"] = "Waiting…"
        shared["last_diff"] = 0.0
