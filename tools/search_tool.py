from typing import List, Dict, Any
from duckduckgo_search import DDGS

def search_vendors(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Performs a free web search for potential vendors using DuckDuckGo.
    
    Args:
        query: Search query (e.g. 'enterprise CRM software vendors')
        max_results: Maximum search results to return.
        
    Returns:
        List of search result dicts (title, href, body).
    """
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "href": r.get("href", ""),
                    "snippet": r.get("body", "")
                })
        return results
    except Exception as e:
        return [{"title": "Search Error", "href": "", "snippet": f"DuckDuckGo search failed: {str(e)}"}]
