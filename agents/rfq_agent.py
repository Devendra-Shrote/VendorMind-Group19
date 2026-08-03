from core.llm import get_nvidia_llm
from core.prompts import RFQ_GENERATOR_PROMPT
from models.schemas import RFQRequirement
from langchain_core.prompts import PromptTemplate

class RFQAgent:
    """Agent responsible for drafting professional RFQ documents."""
    
    def __init__(self, model_name: str = None):
        self.llm = get_nvidia_llm(model_name=model_name)
        self.prompt = PromptTemplate(
            template=RFQ_GENERATOR_PROMPT,
            input_variables=["category", "specifications", "budget", "timeline", "key_criteria"]
        )
        self.chain = self.prompt | self.llm

    def generate_rfq(self, requirement: RFQRequirement) -> str:
        """Generates a detailed RFQ document from requirements."""
        response = self.chain.invoke({
            "category": requirement.category,
            "specifications": requirement.specifications,
            "budget": requirement.budget,
            "timeline": requirement.timeline,
            "key_criteria": ", ".join(requirement.key_criteria) if requirement.key_criteria else "Standard industry standards"
        })
        return response.content
