from bs4 import BeautifulSoup

def compute(html):
    if not html:
        return 0.0
    soup = BeautifulSoup(html, 'html.parser')
    score = 0
    # title
    if soup.title and soup.title.string and 10 < len(soup.title.string) < 70:
        score += 30
    # meta description
    descr = soup.find('meta', attrs={'name':'description'})
    if descr and descr.get('content') and 20 < len(descr.get('content')) < 160:
        score += 25
    # h1 present
    if soup.find('h1'):
        score += 20
    # image alts
    imgs = soup.find_all('img')
    if imgs:
        with_alt = sum(1 for img in imgs if img.get('alt'))
        score += min(15, int((with_alt / len(imgs)) * 15))
    # internal links count
    links = soup.find_all('a', href=True)
    if links and len(links) > 3:
        score += 10
    return min(100.0, score)
