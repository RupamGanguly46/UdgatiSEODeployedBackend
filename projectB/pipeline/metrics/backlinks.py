from urllib.parse import urlparse
import math

def compute(url):
    '''
    Simple proxy for backlink/authority score:
    - Use domain length and presence of popular TLDs to estimate.
    Replace this with Moz/Ahrefs API calls in production.
    '''
    if not url:
        return 0.0
    try:
        host = urlparse(url).netloc or url
        # heuristic: short, well-known hosts get higher score
        parts = host.split('.')
        name = parts[-2] if len(parts) >= 2 else parts[0]
        score = max(10, min(90, 100 - len(name)*2))
        # boost for common giants
        boosters = ['wikipedia','github','stackoverflow','medium','cnn','nytimes','forbes']
        for b in boosters:
            if b in host:
                score = 95.0
        return score
    except Exception:
        return 0.0
