# ⚡ VendorMind: Agentic Procurement System

VendorMind is an intelligent **Agentic Procurement Platform** built for hackathons using **NVIDIA AI Endpoints** (`langchain-nvidia-ai-endpoints`) and **zero paid external APIs**.

---

## 🌟 Key Features

1. **📝 Intelligent RFQ Drafting Agent**: Generates complete, enterprise-grade Request for Quotation (RFQ) documents using `meta/llama-3.3-70b-instruct` or other NVIDIA NIM models.
2. **🌐 Zero-Paid Web Search & Scraping**: Uses `duckduckgo-search` and `beautifulsoup4` + `requests` to gather vendor intelligence without API paywalls.
3. **📄 Proposal & PDF Auditor**: Automated parsing of vendor quotes and PDF proposals with `pypdf`.
4. **📊 Total Cost of Ownership (TCO) Calculator**: Multi-year financial modeling and weighted vendor scoring.
5. **💻 Modern Streamlit Dashboard**: Clean, responsive UI for interactive procurement management.

---

## 📁 Repository Structure

```text
VendorMind1/
├── .env                    # Local environment secrets (NVIDIA_API_KEY)
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore configuration
├── requirements.txt        # Python dependency manifest
├── app.py                  # Main Streamlit dashboard application
├── README.md               # Project documentation
├── config/                 # Application configuration & settings validation
│   ├── __init__.py
│   └── settings.py
├── core/                   # LLM factory & master prompts
│   ├── __init__.py
│   ├── llm.py
│   └── prompts.py
├── agents/                 # Multi-agent orchestrator & specialized agents
│   ├── __init__.py
│   ├── orchestrator.py
│   ├── rfq_agent.py
│   └── vendor_agent.py
├── tools/                  # Free tooling (scraping, search, PDF, scoring)
│   ├── __init__.py
│   ├── pdf_parser.py
│   ├── scorer.py
│   ├── search_tool.py
│   └── web_scraper.py
├── models/                 # Pydantic data schemas
│   ├── __init__.py
│   └── schemas.py
└── ui/                     # UI components & styling
    ├── __init__.py
    └── components.py
```

---

## 🚀 Quickstart Guide

### 1. Clone & Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure NVIDIA API Key

1. Get a free NVIDIA API Key from [NVIDIA Build](https://build.nvidia.com).
2. Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

3. Open `.env` and set your key:

```env
NVIDIA_API_KEY=nvapi-your-actual-key-here
```

### 4. Launch Streamlit Application

```bash
streamlit run app.py
```

---

## 🛠️ Tech Stack

- **LLM Engine**: `langchain-nvidia-ai-endpoints` (`ChatNVIDIA`)
- **Agent Orchestration**: `langchain`, `pydantic`
- **UI & Dashboard**: `streamlit`
- **Web Scraping & Search (Free)**: `beautifulsoup4`, `requests`, `duckduckgo-search`
- **Document Processing**: `pypdf`
