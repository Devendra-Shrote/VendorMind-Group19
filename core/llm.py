import os
from typing import Optional
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from config.settings import settings

def get_nvidia_llm(
    model_name: Optional[str] = None,
    temperature: float = 0.2,
    max_tokens: int = 2048
) -> ChatNVIDIA:
    """
    Factory function to instantiate NVIDIA Hosted LLM via ChatNVIDIA.
    
    Args:
        model_name: NVIDIA Nim model identifier (e.g. meta/llama-3.3-70b-instruct).
        temperature: Sampling temperature for generation.
        max_tokens: Maximum tokens in response.
        
    Returns:
        Configured ChatNVIDIA instance.
    """
    api_key = settings.NVIDIA_API_KEY or os.getenv("NVIDIA_API_KEY")
    selected_model = model_name or settings.DEFAULT_MODEL
    
    if not api_key or api_key == "nvapi-your-actual-key-here":
        raise ValueError("Missing valid NVIDIA_API_KEY in .env file or environment.")
        
    return ChatNVIDIA(
        model=selected_model,
        nvidia_api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens
    )
