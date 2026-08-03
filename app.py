import streamlit as st
from config.settings import settings
from ui.components import render_header, render_sidebar
from agents.orchestrator import ProcurementOrchestrator
from tools.search_tool import search_vendors
from tools.pdf_parser import extract_text_from_pdf

st.set_page_config(
    page_title="VendorMind - Agentic Procurement System",
    page_icon="⚡",
    layout="wide"
)

render_header()
user_key, selected_model = render_sidebar()

# Check API key configuration status
if not settings.validate() and not user_key:
    st.warning("⚠️ Please configure your `NVIDIA_API_KEY` in `.env` or in the sidebar to start using AI features.")

tab1, tab2, tab3, tab4 = st.tabs([
    "📝 RFQ Generator", 
    "🌐 Free Vendor Research", 
    "📄 Quotation / PDF Auditor", 
    "📊 TCO Calculator"
])

with tab1:
    st.header("Draft Request for Quotation (RFQ)")
    st.caption("AI Agent drafts comprehensive RFQs tuned to your specifications.")
    
    col1, col2 = st.columns(2)
    with col1:
        category = st.text_input("Product / Service Category", "Enterprise Cloud Database")
        budget = st.text_input("Target Budget Range", "$50,000 - $80,000 / year")
        timeline = st.text_input("Delivery Timeline", "Q3 2026 (Within 45 Days)")
    with col2:
        specs = st.text_area("Technical Specifications", "High-availability Postgres database, 99.99% SLA,SOC2 compliant, 24/7 support.")
        criteria = st.text_input("Key Criteria (comma separated)", "SLA, Security Compliance, Multi-region Failover")

    if st.button("🚀 Generate RFQ Document", type="primary"):
        with st.spinner("Agent generating RFQ using NVIDIA Nim..."):
            try:
                orchestrator = ProcurementOrchestrator(model_name=selected_model)
                rfq_result = orchestrator.create_rfq(
                    category=category,
                    specs=specs,
                    budget=budget,
                    timeline=timeline,
                    criteria=[c.strip() for c in criteria.split(",") if c.strip()]
                )
                st.subheader("Generated RFQ Document")
                st.markdown(rfq_result)
                st.download_button("📥 Download RFQ (.md)", data=rfq_result, file_name="RFQ_Document.md")
            except Exception as e:
                st.error(f"Error generating RFQ: {str(e)}")

with tab2:
    st.header("Free Vendor Research & Web Scraping")
    st.caption("Performs web search via DuckDuckGo & extracts public vendor web pages without paid APIs.")
    
    query = st.text_input("Search Vendors", "Managed PostgreSQL database providers")
    if st.button("🔍 Search Vendors"):
        with st.spinner("Searching DuckDuckGo..."):
            results = search_vendors(query)
            for idx, r in enumerate(results, 1):
                st.markdown(f"**{idx}. [{r['title']}]({r['href']})**")
                st.write(r['snippet'])
                st.divider()

    st.subheader("Analyze Specific Vendor URL")
    vendor_url = st.text_input("Vendor URL to Scrape & Analyze", "https://www.postgresql.org")
    rfq_context = st.text_area("RFQ Context for Analysis", "Enterprise high-availability database requirements")
    
    if st.button("🤖 Analyze Vendor"):
        with st.spinner("Scraping page & evaluating vendor..."):
            try:
                orchestrator = ProcurementOrchestrator(model_name=selected_model)
                res = orchestrator.analyze_vendor(vendor_url, rfq_context)
                if res["success"]:
                    st.success(f"Scraped and Analyzed {res['vendor_url']}")
                    st.markdown(res["analysis"])
                else:
                    st.error(f"Scraping failed: {res['error']}")
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")

with tab3:
    st.header("Quotation & Proposal PDF Auditor")
    st.caption("Upload vendor proposal PDF for automated text extraction & analysis.")
    
    uploaded_file = st.file_uploader("Upload Vendor Quotation (PDF)", type=["pdf"])
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        res = extract_text_from_pdf(file_bytes)
        if res["success"]:
            st.success(f"Extracted text from {res['num_pages']} page(s).")
            with st.expander("View Extracted Text"):
                st.text(res["text"])
        else:
            st.error(f"PDF extraction error: {res['error']}")

with tab4:
    st.header("Total Cost of Ownership (TCO) & Scoring")
    st.caption("Calculate multi-year TCO and weighted vendor compliance scores.")
    
    c1, c2 = st.columns(2)
    with c1:
        base_cost = st.number_input("Base License / Product Cost ($)", value=50000.0)
        impl_cost = st.number_input("Implementation / Setup Fee ($)", value=10000.0)
        maint_cost = st.number_input("Annual Maintenance / Support ($)", value=5000.0)
        years = st.slider("Contract Horizon (Years)", 1, 5, 3)
    with c2:
        total_maint = maint_cost * years
        tco = base_cost + impl_cost + total_maint
        st.metric("3-Year Total Cost of Ownership", f"${tco:,.2f}")
        st.json({
            "Base Cost": base_cost,
            "Implementation Fee": impl_cost,
            "Annual Maintenance": maint_cost,
            "Years": years,
            "Total TCO": tco
        })
