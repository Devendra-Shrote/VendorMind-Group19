import io
from typing import Dict, Any
from pypdf import PdfReader

def extract_text_from_pdf(file_bytes: bytes) -> Dict[str, Any]:
    """
    Extracts text content from uploaded vendor PDF proposals or quotation documents.
    
    Args:
        file_bytes: Binary contents of uploaded PDF file.
        
    Returns:
        Dict with total pages, extracted text, and extraction status.
    """
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        num_pages = len(reader.pages)
        extracted_text = []
        
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                extracted_text.append(f"--- Page {i+1} ---\n{page_text}")
                
        full_text = "\n\n".join(extracted_text)
        return {
            "success": True,
            "num_pages": num_pages,
            "text": full_text[:8000],  # Truncate for token efficiency
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "num_pages": 0,
            "text": "",
            "error": str(e)
        }
