from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class UserRequirement(BaseModel):
    """
    Structured model representing initial procurement requirements submitted by the user.
    Designed for LangChain structured output parsing.
    """
    model_config = ConfigDict(extra="ignore", json_schema_serialization_defaults_required=True)
    
    project_description: str = Field(
        ..., 
        description="Comprehensive description of the procurement project, objectives, and scope."
    )
    required_features: List[str] = Field(
        ..., 
        min_items=1, 
        description="List of mandatory technical features or deliverables required from vendors."
    )
    budget_limit_inr: float = Field(
        ..., 
        gt=0, 
        description="Maximum budget ceiling in Indian Rupees (INR)."
    )

class VendorQuote(BaseModel):
    """
    Structured model representing extracted vendor quotation data.
    """
    model_config = ConfigDict(extra="ignore", json_schema_serialization_defaults_required=True)
    
    vendor_name: str = Field(
        ..., 
        description="Official name of the vendor or service provider company."
    )
    public_tier_price: float = Field(
        ..., 
        ge=0, 
        description="Public standard catalog/tier price quoted by vendor in INR."
    )
    feature_list: List[str] = Field(
        ..., 
        description="List of features, services, or SLAs included in the vendor quote."
    )
    quote_details: str = Field(
        ..., 
        description="Additional quotation terms, validity period, support tier, or notes."
    )

class CounterOffer(BaseModel):
    """
    Structured model for strategic counter-offers and automated vendor negotiation drafts.
    """
    model_config = ConfigDict(extra="ignore", json_schema_serialization_defaults_required=True)
    
    vendor_name: str = Field(
        ..., 
        description="Name of the targeted vendor for negotiation."
    )
    original_price_inr: float = Field(
        ...,
        ge=0,
        description="Initial price quoted by vendor in INR."
    )
    targeted_reduced_price: float = Field(
        ..., 
        gt=0, 
        description="Proposed counter-offer target price in INR."
    )
    negotiation_rationale: str = Field(
        ..., 
        description="Data-driven justification, market benchmark, or volume argument for price reduction."
    )
    draft_counter_offer_email: str = Field(
        ..., 
        description="Professional, firm, yet collaborative counter-offer email draft addressed to vendor sales."
    )

# Additional legacy/orchestration schemas
class RFQRequirement(BaseModel):
    category: str = Field(..., description="Product or service category")
    specifications: str = Field(..., description="Detailed technical or service specifications")
    budget: str = Field(..., description="Estimated budget or price ceiling")
    timeline: str = Field(..., description="Expected delivery or execution timeframe")
    key_criteria: List[str] = Field(default_factory=list, description="Key selection priorities (e.g. SLA, Price, Warranty)")

class VendorProfile(BaseModel):
    name: str = Field(..., description="Vendor company name")
    website: Optional[str] = Field(None, description="Vendor website URL")
    summary: str = Field(..., description="Brief company and product summary")
    pricing_model: Optional[str] = Field(None, description="Pricing structure (Subscription, One-time, Volume)")
    compliance_score: float = Field(0.0, description="Compliance score from 0 to 100")
    pros: List[str] = Field(default_factory=list)
    cons: List[str] = Field(default_factory=list)
    risk_level: str = Field("Medium", description="Low, Medium, or High risk assessment")

class ProposalComparison(BaseModel):
    rfq_title: str
    vendors_evaluated: List[VendorProfile]
    top_recommendation: str
    decision_rationale: str
