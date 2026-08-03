from typing import Dict, Any
from core.llm import get_nvidia_llm
from core.prompts import VENDOR_ANALYSIS_PROMPT
from tools.web_scraper import scrape_vendor_website
from langchain_core.prompts import PromptTemplate

class VendorAnalysisAgent:
    """Agent responsible for researching and evaluating vendors."""
    
    def __init__(self, model_name: str = None):
        self.llm = get_nvidia_llm(model_name=model_name)
        self.prompt = PromptTemplate(
            template=VENDOR_ANALYSIS_PROMPT,
            input_variables=["vendor_raw_data", "rfq_requirements"]
        )
        self.chain = self.prompt | self.llm

    def evaluate_vendor_url(self, vendor_url: str, rfq_requirements: str) -> Dict[str, Any]:
        """Scrapes vendor URL and runs LLM evaluation against requirements."""
        scrape_result = scrape_vendor_website(vendor_url)
        
        if not scrape_result["success"]:
            return {
                "vendor_url": vendor_url,
                "success": False,
                "error": scrape_result["error"],
                "analysis": None
            }
            
        raw_data = f"Title: {scrape_result['title']}\nContent: {scrape_result['content']}"
        
        response = self.chain.invoke({
            "vendor_raw_data": raw_data,
            "rfq_requirements": rfq_requirements
        })
        
        return {
            "vendor_url": vendor_url,
            "success": True,
            "error": None,
            "analysis": response.content
        }
