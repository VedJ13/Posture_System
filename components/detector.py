import streamlit as st

def ensure_auth_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user_name" not in st.session_state:
        st.session_state.user_name = "Ved"

def render_auth_gate():
    st.title("🧘 PostureSense")
    st.subheader("Login / Sign Up")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)
            if submitted:
                if email and password:
                    st.session_state.logged_in = True
                    st.session_state.user_name = email.split("@")[0].title()
                    st.success("Login successful")
                    st.rerun()
                else:
                    st.error("Enter email and password.")

    with tab2:
        with st.form("signup_form"):
            name = st.text_input("Full name")
            email = st.text_input("Create email")
            password = st.text_input("Create password", type="password")
            submitted = st.form_submit_button("Create account", use_container_width=True)
            if submitted:
                if name and email and password:
                    st.session_state.logged_in = True
                    st.session_state.user_name = name
                    st.success("Account created")
                    st.rerun()
                else:
                    st.error("Fill all fields.")
