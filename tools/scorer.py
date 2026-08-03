from typing import Dict, Any

def calculate_tco(base_cost: float, implementation_fee: float = 0.0, annual_maintenance: float = 0.0, years: int = 3) -> Dict[str, Any]:
    """
    Calculates Total Cost of Ownership (TCO) across a multi-year horizon.
    """
    total_recurring = annual_maintenance * years
    tco = base_cost + implementation_fee + total_recurring
    
    return {
        "base_cost": base_cost,
        "implementation_fee": implementation_fee,
        "annual_maintenance": annual_maintenance,
        "years": years,
        "total_cost_of_ownership": round(tco, 2)
    }

def calculate_vendor_score(price_score: float, technical_score: float, compliance_score: float, weights: Dict[str, float] = None) -> float:
    """
    Computes weighted evaluation score (0 to 100).
    """
    if weights is None:
        weights = {"price": 0.4, "technical": 0.4, "compliance": 0.2}
        
    final_score = (
        (price_score * weights.get("price", 0.4)) +
        (technical_score * weights.get("technical", 0.4)) +
        (compliance_score * weights.get("compliance", 0.2))
    )
    return round(final_score, 2)
