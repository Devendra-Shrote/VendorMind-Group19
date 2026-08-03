import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Centralized configuration manager for VendorMind."""
    
    NVIDIA_API_KEY: str = os.getenv("NVIDIA_API_KEY", "")
    DEFAULT_MODEL: str = os.getenv("NVIDIA_MODEL_NAME", "meta/llama-3.3-70b-instruct")
    
    @classmethod
    def validate(cls) -> bool:
        """Check if essential environment variables are configured."""
        if not cls.NVIDIA_API_KEY or cls.NVIDIA_API_KEY == "nvapi-your-nvidia-api-key-here":
            return False
        return True

settings = Settings()
