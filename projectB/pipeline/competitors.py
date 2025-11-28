import os
import httpx

async def find_competitors(keywords, max_candidates=30):
    SERPAPI_KEY = os.getenv('SERPAPI_KEY')
    print(keywords)
    '''
    If SERPAPI_KEY present, attempt to use SerpAPI (simple search per keyword).
    Otherwise, return a canned list of well-known domains (excluding exact duplicates later).
    '''
    if SERPAPI_KEY:
        # Simple SerpAPI call per keyword (requires key and internet)
        results = set()
        async with httpx.AsyncClient() as client:
            for kw in keywords[:10]:
                params = {
                    'q': kw,
                    'api_key': SERPAPI_KEY,
                    'engine': 'google'
                }
                try:
                    r = await client.get('https://serpapi.com/search', params=params, timeout=10)
                    data = r.json()
                    for res in data.get('organic_results', []):
                        link = res.get('link') or res.get('formattedUrl')
                        if link:
                            results.add(link)
                except Exception:
                    print("Exception")
                    continue
                if len(results) >= max_candidates:
                    break
        return list(results)[:max_candidates]
    else:
        # canned fallback
        sample = [
            "https://wikipedia.org",
            "https://mozilla.org",
            "https://github.com",
            "https://stackoverflow.com",
            "https://medium.com",
            "https://cnn.com",
            "https://nytimes.com",
            "https://techcrunch.com",
            "https://forbes.com",
        ]
        return sample[:max_candidates]
