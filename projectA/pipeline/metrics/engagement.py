from urllib.parse import urlparse
def compute(url):
    '''
    Proxy engagement by assigning higher score to known big sites.
    Replace with SimilarWeb / Google Analytics integration for real data.
    '''
    if not url:
        return 0.0
    host = urlparse(url).netloc
    boosters = {
        'wikipedia.org':95, 'github.com':92, 'stackoverflow.com':90,
        'medium.com':70, 'cnn.com':85, 'nytimes.com':88, 'forbes.com':80
    }
    for k,v in boosters.items():
        if k in host:
            return float(v)
    # default small-site estimate
    return 30.0
