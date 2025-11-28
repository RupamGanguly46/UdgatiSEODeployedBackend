import httpx
from bs4 import BeautifulSoup
import asyncio

UA = "Mozilla/5.0 (compatible; SimpleSEO/1.0; +https://example.com/bot)"

async def fetch_page(url, timeout=10.0):
    '''
    Fetches the page and returns (html, text_content)
    If fetching fails, returns (None, '').
    '''
    try:
        async with httpx.AsyncClient(timeout=timeout, headers={'User-Agent': UA}) as client:
            r = await client.get(url)
            r.raise_for_status()
            html = r.text
            soup = BeautifulSoup(html, "html.parser")
            # remove scripts and styles
            for s in soup(["script", "style", "noscript"]):
                s.decompose()
            text = soup.get_text(separator=" ", strip=True)
            return html, text
    except Exception as e:
        # fallback minimal empty result
        print(e)
        return None, ""
