from difflib import SequenceMatcher
def compute(textA, textB, keywords):
    if not textA or not textB:
        return 0.0
    # lightweight similarity using sequence matcher on shorter excerpts
    a = textA[:2000]
    b = textB[:2000]
    ratio = SequenceMatcher(None, a, b).ratio()  # 0..1
    return ratio * 100.0
