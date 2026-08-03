import streamlit as st

def render_header():
    """Renders top header and badge for VendorMind."""
    st.markdown("""
        <div style="background: linear-gradient(90deg, #0052D4, #4364F7, #6FB1FC); padding: 24px; border-radius: 12px; margin-bottom: 24px;">
            <h1 style="color: white; margin: 0;">⚡ VendorMind</h1>
            <p style="color: #e0e0e0; margin: 4px 0 0 0;">Agentic Procurement System — Powered by NVIDIA AI Endpoints & LangChain</p>
        </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Renders sidebar controls and API status."""
    st.sidebar.title("⚙️ System Status")
    api_key = st.sidebar.text_input("NVIDIA API Key", type="password", help="Loaded from .env by default")
    model_choice = st.sidebar.selectbox(
        "NVIDIA Model",
        [
            "meta/llama-3.3-70b-instruct",
            "nvidia/nemotron-4-340b-instruct",
            "mistralai/mistral-large-2-instruct"
        ]
    )
    st.sidebar.divider()
    st.sidebar.markdown("**Zero Paid APIs Mode**")
    st.sidebar.caption("✅ BeautifulSoup Web Scraper")
    st.sidebar.caption("✅ DuckDuckGo Search")
    st.sidebar.caption("✅ PyPDF Document Extractor")
    return api_key, model_choice
