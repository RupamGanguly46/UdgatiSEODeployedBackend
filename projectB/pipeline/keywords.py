import re
from collections import Counter

def extract_keywords(text, topn=30):
    '''
    Very simple keyword extractor: split words, remove short words, return topn frequent words.
    Replace this with YAKE/KeyBERT for production.
    '''
    if not text:
        return []
    words = re.findall(r"\w+", text.lower())
    words = [w for w in words if len(w) > 3]
    c = Counter(words)
    return [w for w,_ in c.most_common(topn)]
