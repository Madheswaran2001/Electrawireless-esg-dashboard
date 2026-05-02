import streamlit as st
import os

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ElectraWireless ESG Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Hide Streamlit default chrome for a cleaner embed ─────────────────────────
st.markdown("""
    <style>
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }
    </style>
""", unsafe_allow_html=True)

# ── Locate dashboard.html robustly ────────────────────────────────────────────
# Works whether you run locally or deploy on Streamlit Cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(BASE_DIR, "electrawireless_esg_dashboard.html")

if not os.path.exists(HTML_FILE):
    st.error(
        f"❌ Could not find **electrawireless_esg_dashboard.html**.\n\n"
        f"Expected location: `{HTML_FILE}`\n\n"
        f"Make sure `electrawireless_esg_dashboard.html` is in the **same folder** as `app.py` "
        f"and that both files are committed to your GitHub repository."
    )
    st.stop()

# ── Load and render the HTML dashboard ────────────────────────────────────────
with open(HTML_FILE, "r", encoding="utf-8") as f:
    html_content = f.read()

st.components.v1.html(html_content, height=1000, scrolling=True)
