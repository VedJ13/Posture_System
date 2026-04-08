import streamlit as st

def apply_global_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

    :root{
        --good:#00e676;
        --warn:#ffea00;
        --bad:#ff1744;
        --bg:#0d0f14;
        --card:#161922;
        --text:#e8eaf0;
        --muted:#6b7280;
        --line:#1e2230;
    }

    html,body,[data-testid="stAppViewContainer"]{
        background:var(--bg)!important;
        color:var(--text)!important;
        font-family:'DM Sans',sans-serif
    }

    [data-testid="stSidebar"]{
        background:#0a0c10!important;
        border-right:1px solid var(--line)
    }

    h1,h2,h3{
        font-family:'Space Mono',monospace
    }

    #MainMenu,footer,header{
        visibility:hidden;
    }
    </style>
    """, unsafe_allow_html=True)
