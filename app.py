import streamlit as st
from components.styles import apply_global_styles
from components.state import init_app_state

st.set_page_config(page_title="Exercises", page_icon="🏃", layout="wide", initial_sidebar_state="expanded")
apply_global_styles()
init_app_state()

if not st.session_state.get("logged_in", False):
    st.warning("Please log in from the home page.")
    st.stop()

st.title("🏃 Posture Correction Exercises")
st.caption("Simple exercises to improve upper-back posture, shoulder alignment, and neck position.")

exercises = [
    ("Chin Tucks", "Stand tall, pull your chin straight back, hold 5 seconds, repeat 10 times."),
    ("Wall Angels", "Stand against a wall, slide arms up and down while keeping elbows and wrists close to wall."),
    ("Thoracic Extensions", "Sit upright and gently extend your upper back over the chair support."),
    ("Scapular Retractions", "Pull shoulder blades back and down, hold 3 seconds, repeat 12 times."),
    ("Doorway Chest Stretch", "Place forearms on a doorway and lean forward to open tight chest muscles."),
    ("Cat-Cow", "Alternate between rounding and extending the spine slowly for mobility."),
]
for name, desc in exercises:
    st.markdown(f"<div class='tip'><b>{name}</b><br>{desc}</div>", unsafe_allow_html=True)

st.markdown("### Daily routine")
st.write("Do 5–10 minutes daily. Combine mobility, stretching, and awareness during screen work.")
