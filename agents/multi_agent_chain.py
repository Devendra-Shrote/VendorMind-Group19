import os
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from models.schemas import UserRequirement, VendorQuote, CounterOffer

load_dotenv()

def get_llama_llm() -> ChatNVIDIA:
    """Initializes ChatNVIDIA strictly with meta/llama-3.1-70b-instruct."""
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key or api_key.startswith("nvapi-your-"):
        raise ValueError("Missing or unconfigured NVIDIA_API_KEY in environment variables or .env file.")
    return ChatNVIDIA(
        model="meta/llama-3.1-70b-instruct",
        nvidia_api_key=api_key,
        temperature=0.2,
        max_tokens=2048
    )

# --- AGENT PROMPT TEMPLATES ---

SCOUT_AGENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are the Senior Scout Agent for VendorMind.
Your role is to scan vendor search results, pricing tiers, and public catalog data against the user's budget and requirements.

Analyze the input vendor intelligence and summarize:
1. Vendor Name & Public Pricing Tiers (in INR or converted equivalent)
2. Alignment with required technical features
3. Budget feasibility check (User Budget Limit: ₹{budget_limit_inr:,.2f})
"""),
    ("human", """User Requirements:
Project: {project_description}
Required Features: {required_features}
Max Budget (INR): ₹{budget_limit_inr:,.2f}

Vendor Intelligence / Search Scrapes:
{vendor_raw_data}
""")
])

EVALUATION_AGENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are the Chief Evaluation Agent for VendorMind.
Your role is to perform rigorous gap analysis between vendor offerings and user requirements.

Analyze the Scout Agent's findings and identify:
1. Pricing Gaps: Calculate exact over-budget deltas or tier mismatches (in INR).
2. Feature Gaps: Missing required features, missing enterprise SLAs, or hidden costs.
3. Vendor Leverage Points: Features missing from vendor, competitive benchmarks, or market weaknesses.
"""),
    ("human", """User Budget (INR): ₹{budget_limit_inr:,.2f}
Required Features: {required_features}

Scout Agent Report:
{scout_summary}
""")
])

NEGOTIATOR_AGENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are the Executive Negotiator Agent for VendorMind.
Your task is to take the Evaluation Agent's gap analysis and formulate a winning negotiation strategy.

Produce:
1. Targeted Reduced Counter-Offer Price (INR)
2. Strategic Rationale (leveraging feature gaps, volume commitment, or competitor pricing)
3. Formal Vendor Negotiation Email Draft addressed to Vendor Sales Manager.
"""),
    ("human", """Vendor Name: {vendor_name}
Original Quoted Price (INR): ₹{original_price_inr:,.2f}
User Budget Limit (INR): ₹{budget_limit_inr:,.2f}

Evaluation Gap Analysis:
{evaluation_report}
""")
])


class ProcurementMultiAgentChain:
    """
    Sequential Multi-Agent Procurement Chain using ChatNVIDIA (meta/llama-3.1-70b-instruct).
    Connects Scout Agent -> Evaluation Agent -> Negotiator Agent seamlessly.
    """
    
    def __init__(self, api_key: str = None):
        if api_key:
            os.environ["NVIDIA_API_KEY"] = api_key
            
        self.llm = get_llama_llm()
        
        # 1. Scout Agent Chain
        self.scout_chain = SCOUT_AGENT_PROMPT | self.llm | StrOutputParser()
        
        # 2. Evaluation Agent Chain
        self.eval_chain = EVALUATION_AGENT_PROMPT | self.llm | StrOutputParser()
        
        # 3. Negotiator Agent Chain (Structured Pydantic Output)
        self.negotiator_structured_agent = self.llm.with_structured_output(CounterOffer)
        # Text version for fallback or complete prompt chain
        self.negotiator_text_chain = NEGOTIATOR_AGENT_PROMPT | self.llm | StrOutputParser()

    def run_full_pipeline(
        self, 
        user_req: UserRequirement, 
        vendor_data: str, 
        vendor_name: str = "Vendor", 
        original_price_inr: float = 0.0
    ) -> Dict[str, Any]:
        """
        Executes end-to-end multi-agent procurement workflow:
        Step 1: Scout Agent analyzes raw intelligence
        Step 2: Evaluation Agent identifies pricing/feature gaps
        Step 3: Negotiator Agent generates counter-offer and negotiation email draft
        """
        # Step 1: Run Scout Agent
        print("🔍 Step 1: Scout Agent analyzing vendor intelligence...")
        scout_summary = self.scout_chain.invoke({
            "project_description": user_req.project_description,
            "required_features": ", ".join(user_req.required_features),
            "budget_limit_inr": user_req.budget_limit_inr,
            "vendor_raw_data": vendor_data
        })
        
        # Step 2: Run Evaluation Agent
        print("📊 Step 2: Evaluation Agent conducting gap analysis...")
        evaluation_report = self.eval_chain.invoke({
            "budget_limit_inr": user_req.budget_limit_inr,
            "required_features": ", ".join(user_req.required_features),
            "scout_summary": scout_summary
        })
        
        # Step 3: Run Negotiator Agent
        print("🤝 Step 3: Negotiator Agent drafting counter-offer & proposal...")
        negotiation_text = self.negotiator_text_chain.invoke({
            "vendor_name": vendor_name,
            "original_price_inr": original_price_inr or user_req.budget_limit_inr * 1.2,
            "budget_limit_inr": user_req.budget_limit_inr,
            "evaluation_report": evaluation_report
        })
        
        # Optionally attempt structured Pydantic extraction for counter offer schema
        structured_counter_offer = None
        try:
            structured_counter_offer = self.negotiator_structured_agent.invoke(
                f"Extract structured counter offer for vendor '{vendor_name}' with original price ₹{original_price_inr}:\n{negotiation_text}"
            )
        except Exception:
            # Fall back to text parsing if structured extraction hits token/formatting constraint
            pass

        return {
            "scout_summary": scout_summary,
            "evaluation_report": evaluation_report,
            "negotiation_text": negotiation_text,
            "structured_counter_offer": structured_counter_offer
        }


# Direct execution example
if __name__ == "__main__":
    print("⚡ VendorMind Multi-Agent Procurement Chain (ChatNVIDIA Llama-3.1-70B)")
    
    # Sample Test Data
    sample_user_req = UserRequirement(
        project_description="Enterprise CRM Software with Automated Lead Scoring & Custom Workflows",
        required_features=["Automated Lead Scoring", "Custom Pipeline Workflows", "API Integration", "24/7 SLA Support"],
        budget_limit_inr=500000.0  # ₹5 Lakhs
    )
    
    sample_vendor_scrapes = """
    Vendor Name: CloudScale CRM Enterprise
    Quoted Public Price: ₹7,50,000 / year ($9,000 USD)
    Features Included: Automated Lead Scoring, API Integration, Standard Email Support (5x8).
    Missing / Add-on Features: 24/7 SLA Support requires Enterprise Platinum Add-on (+₹1,50,000).
    """

    try:
        pipeline = ProcurementMultiAgentChain()
        result = pipeline.run_full_pipeline(
            user_req=sample_user_req,
            vendor_data=sample_vendor_scrapes,
            vendor_name="CloudScale CRM Enterprise",
            original_price_inr=750000.0
        )

        print("\n" + "="*50)
        print("1. SCOUT AGENT SUMMARY:\n", result["scout_summary"])
        print("="*50)
        print("2. EVALUATION AGENT REPORT:\n", result["evaluation_report"])
        print("="*50)
        print("3. NEGOTIATOR AGENT PROPOSAL:\n", result["negotiation_text"])
        print("="*50)
    except Exception as err:
        print("Pipeline Execution Note:", err)
