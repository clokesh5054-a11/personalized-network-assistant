import requests
import urllib.parse

def verify_fact_wikipedia(query: str) -> dict:
    """
    Search Wikipedia for the given query, fetch the summary of the top result,
    and return the title, extract, and canonical URL.
    """
    if not query or not query.strip():
        return {"found": False, "message": "Query cannot be empty."}
        
    search_url = "https://en.wikipedia.org/w/api.php"
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "utf8": 1
    }
    
    try:
        response = requests.get(search_url, params=search_params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        search_results = data.get("query", {}).get("search", [])
        if not search_results:
            return {"found": False, "message": f"No Wikipedia articles found matching '{query}'."}
            
        top_title = search_results[0]["title"]
        
        # Fetch the introduction text
        extract_params = {
            "action": "query",
            "prop": "extracts",
            "exintro": 1,
            "explaintext": 1,
            "titles": top_title,
            "format": "json",
            "redirects": 1
        }
        
        extract_response = requests.get(search_url, params=extract_params, timeout=10)
        extract_response.raise_for_status()
        extract_data = extract_response.json()
        
        pages = extract_data.get("query", {}).get("pages", {})
        if not pages:
            return {"found": False, "message": f"Could not retrieve details for '{top_title}'."}
            
        page_id = list(pages.keys())[0]
        if page_id == "-1":
            return {"found": False, "message": f"No details found for '{top_title}'."}
            
        page_info = pages[page_id]
        title = page_info.get("title", top_title)
        extract = page_info.get("extract", "").strip()
        
        encoded_title = urllib.parse.quote(title.replace(" ", "_"))
        url = f"https://en.wikipedia.org/wiki/{encoded_title}"
        
        if not extract:
            extract = "No summary available for this page."
            
        return {
            "found": True,
            "title": title,
            "summary": extract,
            "url": url
        }
    except requests.exceptions.RequestException as e:
        return {
            "found": False,
            "message": f"Error connecting to Wikipedia API: {str(e)}"
        }
