from bs4 import BeautifulSoup

def compute(url, html):
    '''
    Quick technical checks:
    - HTTPS present in URL
    - mobile meta viewport
    - presence of charset
    - small heuristic mapping -> 0..100
    '''
    score = 0
    if not url:
        return 0.0
    if url.startswith('https'):
        score += 30
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        # viewport
        if soup.find('meta', attrs={'name':'viewport'}):
            score += 25
        # charset
        if soup.find('meta', attrs={'charset':True}) or soup.find('meta', attrs={'http-equiv':'Content-Type'}):
            score += 15
        # robots meta present
        if soup.find('meta', attrs={'name':'robots'}):
            score += 5
        # simple page size heuristic
        text_len = len(soup.get_text(strip=True))
        if text_len < 2000:
            score += 10
        else:
            score += 5
    return min(100.0, score)
