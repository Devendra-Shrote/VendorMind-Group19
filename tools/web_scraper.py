import requests
from bs4 import BeautifulSoup
from typing import Dict, Any

def scrape_vendor_website(url: str, timeout: int = 10) -> Dict[str, Any]:
    """
    Scrapes text content from a vendor's public web page without paid external APIs.
    
    Args:
        url: Target website URL.
        timeout: HTTP request timeout in seconds.
        
    Returns:
        Dict containing title, extracted text, and status code or error.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }
    
    try:
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
            
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove script, style, and navigation noise
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
            
        text = soup.get_text(separator=" ", strip=True)
        title = soup.title.string if soup.title else "No Title Found"
        
        # Return cleaned text truncated to 4000 characters for token efficiency
        return {
            "success": True,
            "url": url,
            "title": title,
            "content": text[:4000],
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "url": url,
            "title": "",
            "content": "",
            "error": str(e)
        }
