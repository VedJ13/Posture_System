import streamlit as st

def apply_global_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');
    :root{--good:#00e676;--warn:#ffea00;--bad:#ff1744;--bg:#0d0f14;--card:#161922;--text:#e8eaf0;--muted:#6b7280;--line:#1e2230}
    html,body,[data-testid="stAppViewContainer"]{background:var(--bg)!important;color:var(--text)!important;font-family:'DM Sans',sans-serif}
    [data-testid="stSidebar"]{background:#0a0c10!important;border-right:1px solid var(--line)}
    h1,h2,h3{font-family:'Space Mono',monospace}
    #MainMenu,footer,header{visibility:hidden;}
    .card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:1rem 1.1rem;margin-bottom:1rem}
    .metric-card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1rem;text-align:center}
    .metric-label{font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
    .metric-value{font-family:'Space Mono',monospace;font-size:1.8rem;font-weight:700}
    .good{color:var(--good)} .warn{color:var(--warn)} .bad{color:var(--bad)} .muted{color:var(--muted)}
    .pill{display:inline-block;padding:.35rem .9rem;border-radius:999px;font-family:'Space Mono',monospace;font-size:.82rem;font-weight:700;letter-spacing:.05em}
    .pg{background:rgba(0,230,118,.15);color:var(--good);border:1px solid rgba(0,230,118,.3)}
    .pw{background:rgba(255,234,0,.12);color:var(--warn);border:1px solid rgba(255,234,0,.3)}
    .pb{background:rgba(255,23,68,.15);color:var(--bad);border:1px solid rgba(255,23,68,.3)}
    .pi{background:rgba(107,114,128,.15);color:var(--muted);border:1px solid rgba(107,114,128,.3)}
    .tip{background:linear-gradient(135deg,#161922 60%,#1a1f2e);border-left:3px solid var(--good);border-radius:0 8px 8px 0;padding:.75rem 1rem;font-size:.9rem;color:#b0bcc8;margin-bottom:.45rem}
    .warn-banner{background:rgba(255,23,68,.12);border:1px solid rgba(255,23,68,.3);border-radius:8px;padding:.7rem 1rem;color:#ff6b8a;font-size:.88rem;margin-bottom:.8rem}
    .section{font-family:'Space Mono',monospace;font-size:.75rem;letter-spacing:.15em;text-transform:uppercase;color:var(--muted);border-bottom:1px solid var(--line);padding-bottom:.35rem;margin:1rem 0 .8rem}
    </style>
    """, unsafe_allow_html=True)
