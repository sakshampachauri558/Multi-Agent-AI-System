from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise RuntimeError(
        "TAVILY_API_KEY is not set. Add it to your .env file "
        "(see .env in the project root)."
    )

tavily = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic. Returns Titles, URLs and snippets."""
    try:
        results = tavily.search(query=query, max_results=5)
    except Exception as e:
        return f"Web search failed: {e}"

    out = []
    for r in results.get("results", []):
        out.append(
            f"Title: {r.get('title', 'N/A')}\n"
            f"URL: {r.get('url', 'N/A')}\n"
            f"Snippet: {r.get('content', '')[:300]}\n"
        )

    if not out:
        return "No search results found."

    return "\n----\n".join(out)


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        return text[:3000] if text else "No readable content found on this page."
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
