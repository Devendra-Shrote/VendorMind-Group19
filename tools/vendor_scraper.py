import re
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
from duckduckgo_search import DDGS

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

def search_vendor_pricing_pages(vendor_or_category: str, max_results: int = 3) -> List[Dict[str, str]]:
    """
    Finds public pricing page URLs for a vendor or software category using free DuckDuckGo search.
    """
    query = f"{vendor_or_category} pricing plans features tiers cost"
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                href = r.get("href", "")
                title = r.get("title", "")
                snippet = r.get("body", "")
                if href:
                    results.append({"url": href, "title": title, "snippet": snippet})
    except Exception as e:
        results.append({"url": "", "title": "Search Error", "snippet": str(e)})
    return results


def scrape_vendor_pricing_page(url: str, timeout: int = 12) -> Dict[str, Any]:
    """
    Scrapes a vendor pricing web page and extracts pricing tiers, price points, and feature lists.
    No paid APIs required.
    
    Args:
        url: Target web page URL.
        timeout: Maximum request timeout in seconds.
        
    Returns:
        Dict with clean summary text, extracted pricing highlights, features, and metadata.
    """
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove non-content elements
        for noise in soup(["script", "style", "svg", "nav", "footer", "iframe", "header", "form", "noscript"]):
            noise.decompose()
            
        page_title = soup.title.string.strip() if soup.title and soup.title.string else "Vendor Pricing Page"
        
        # 1. Extract Pricing Tables and Cards
        pricing_cards = []
        pricing_selectors = [
            "[class*='price']", "[class*='pricing']", "[class*='tier']", "[class*='plan']",
            "[id*='price']", "[id*='pricing']", "[id*='tier']", "[id*='plan']", "table"
        ]
        
        for selector in pricing_selectors:
            elements = soup.select(selector)
            for el in elements:
                text = el.get_text(separator=" ", strip=True)
                # Keep text snippets that mention price indicators ($ / ₹ / € / month / year / tier / plan)
                if re.search(r"(\$|₹|€|£|USD|INR|per|month|mo|year|yr|free|pro|enterprise)", text, re.IGNORECASE):
                    if len(text) > 20 and len(text) < 1500:
                        pricing_cards.append(text)
                        
        # Deduplicate pricing cards
        unique_pricing_blocks = list(dict.fromkeys(pricing_cards))[:6]
        
        # 2. Extract Feature Bullet Points
        features = []
        for li in soup.find_all("li"):
            feat_text = li.get_text(separator=" ", strip=True)
            if 10 <= len(feat_text) <= 200:
                features.append(feat_text)
                
        deduped_features = list(dict.fromkeys(features))[:15]
        
        # 3. Clean full body text for LLM fallback
        full_text = soup.get_text(separator="\n", strip=True)
        # Collapse multiple blank lines
        clean_full_text = re.sub(r"\n\s*\n", "\n", full_text)
        
        # Construct structured summary block for LLM prompt context
        summary_lines = [
            f"=== VENDOR PRICING SUMMARY ===",
            f"Page Title: {page_title}",
            f"URL: {url}",
            "\n--- DETECTED PRICING TIERS & PLANS ---"
        ]
        
        if unique_pricing_blocks:
            for idx, block in enumerate(unique_pricing_blocks, 1):
                summary_lines.append(f"[Tier/Plan Block {idx}]: {block}")
        else:
            summary_lines.append("No explicit pricing tables detected. Raw page content available below.")
            
        summary_lines.append("\n--- EXTRACTED FEATURE HIGHLIGHTS ---")
        if deduped_features:
            for feat in deduped_features:
                summary_lines.append(f"• {feat}")
        else:
            summary_lines.append("No bulleted feature lists found.")

        summary_lines.append("\n--- CLEAN PAGE TEXT (TRUNCATED FOR LLM) ---")
        summary_lines.append(clean_full_text[:3000])

        clean_llm_summary = "\n".join(summary_lines)
        
        return {
            "success": True,
            "url": url,
            "page_title": page_title,
            "pricing_blocks": unique_pricing_blocks,
            "features": deduped_features,
            "clean_llm_summary": clean_llm_summary,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "url": url,
            "page_title": "",
            "pricing_blocks": [],
            "features": [],
            "clean_llm_summary": f"Failed to scrape pricing page '{url}': {str(e)}",
            "error": str(e)
        }


def get_vendor_pricing_intelligence(vendor_or_category: str) -> Dict[str, Any]:
    """
    High-level end-to-end free pricing intelligence tool.
    1. Searches DuckDuckGo for public pricing pages.
    2. Scrapes the top matching URL.
    3. Returns structured data and clean text summary for LLM analysis.
    """
    search_results = search_vendor_pricing_pages(vendor_or_category, max_results=3)
    
    valid_urls = [r["url"] for r in search_results if r.get("url")]
    
    if not valid_urls:
        return {
            "vendor_query": vendor_or_category,
            "status": "No URLs Found",
            "search_results": search_results,
            "scraped_data": None,
            "summary_for_llm": f"No pricing pages found for search query: '{vendor_or_category}'"
        }
        
    target_url = valid_urls[0]
    scraped_data = scrape_vendor_pricing_page(target_url)
    
    return {
        "vendor_query": vendor_or_category,
        "status": "Success" if scraped_data["success"] else "Scrape Error",
        "search_results": search_results,
        "scraped_data": scraped_data,
        "summary_for_llm": scraped_data["clean_llm_summary"]
    }
