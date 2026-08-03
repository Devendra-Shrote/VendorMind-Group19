from agents.rfq_agent import RFQAgent
from agents.vendor_agent import VendorAnalysisAgent
from models.schemas import RFQRequirement

class ProcurementOrchestrator:
    """Master orchestrator connecting RFQ generation, Vendor Research, and Scoring."""
    
    def __init__(self, model_name: str = None):
        self.rfq_agent = RFQAgent(model_name=model_name)
        self.vendor_agent = VendorAnalysisAgent(model_name=model_name)

    def create_rfq(self, category: str, specs: str, budget: str, timeline: str, criteria: list) -> str:
        req = RFQRequirement(
            category=category,
            specifications=specs,
            budget=budget,
            timeline=timeline,
            key_criteria=criteria
        )
        return self.rfq_agent.generate_rfq(req)

    def analyze_vendor(self, vendor_url: str, rfq_requirements: str):
        return self.vendor_agent.evaluate_vendor_url(vendor_url, rfq_requirements)
