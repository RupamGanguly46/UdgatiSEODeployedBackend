# from .metrics import content, backlinks, technical, onpage, engagement
# from urllib.parse import urlparse

# PROCESS_WEIGHTS = {
#     "content_similarity": 0.25,
#     "backlinks": 0.30,
#     "technical": 0.20,
#     "onpage": 0.15,
#     "engagement": 0.10,
# }

# def normalize(v):
#     if v is None:
#         return 0.0
#     try:
#         v = float(v)
#     except Exception:
#         return 0.0
#     return max(0.0, min(100.0, v))

# def score_entry(entry, target_text, target_keywords):
#     # compute raw process scores using metric modules
#     url = entry['url']
#     html = entry.get('html')
#     text = entry.get('text', '')

#     scores = {}
#     scores['content_similarity'] = content.compute(text, target_text, target_keywords)
#     scores['backlinks'] = backlinks.compute(url)
#     scores['technical'] = technical.compute(url, html)
#     scores['onpage'] = onpage.compute(html)
#     scores['engagement'] = engagement.compute(url)

#     # normalize
#     for k in scores:
#         scores[k] = normalize(scores[k])

#     # weighted aggregate
#     final = 0.0
#     for k,w in PROCESS_WEIGHTS.items():
#         final += scores.get(k,0.0) * w
#     entry['scores'] = scores
#     entry['final_score'] = round(final,2)
#     return entry

# def score_all(entries, target_url, target_text, target_keywords):
#     scored = []
#     for e in entries:
#         scored.append(score_entry(e, target_text, target_keywords))
#     # include the target as well (score itself)
#     # sort by final_score desc
#     scored_sorted = sorted(scored, key=lambda x: x['final_score'], reverse=True)
#     # assign ranks
#     for i, s in enumerate(scored_sorted, start=1):
#         s['rank'] = i
#     return scored_sorted

from .metrics import content, backlinks, technical, onpage, engagement

PROCESS_WEIGHTS = {
    "content_similarity": 0.25,
    "backlinks": 0.30,
    "technical": 0.20,
    "onpage": 0.15,
    "engagement": 0.10,
}

def normalize(v):
    if v is None:
        return None
    try:
        v = float(v)
    except:
        return None
    return max(0.0, min(100.0, v))

def score_entry(entry, target_text, target_keywords):
    url = entry['url']
    html = entry.get('html')
    text = entry.get('text', '')

    skip = entry.get('_skip_metrics', [])

    # Compute raw metric values (None where skipped)
    scores = {
        "content_similarity": None if "content_similarity" in skip else content.compute(text, target_text, target_keywords),
        "backlinks": None if "backlinks" in skip else backlinks.compute(url),
        "technical": None if "technical" in skip else technical.compute(url, html),
        "onpage": None if "onpage" in skip else onpage.compute(html),
        "engagement": None if "engagement" in skip else engagement.compute(url),
    }

    # Normalize (with None preserved)
    for k in scores:
        scores[k] = normalize(scores[k])

    # Compute new total weights only for available metrics
    usable_weight_sum = sum(PROCESS_WEIGHTS[k] for k in PROCESS_WEIGHTS if scores[k] is not None)

    # If nothing usable, fail gracefully
    if usable_weight_sum == 0:
        entry["scores"] = scores
        entry["final_score"] = 0.0
        return entry

    # Recompute weighted score with scaled weights
    final = 0.0
    for k, w in PROCESS_WEIGHTS.items():
        if scores[k] is None:
            continue
        scaled_w = w / usable_weight_sum
        final += scores[k] * scaled_w

    entry["scores"] = scores
    entry["final_score"] = round(final, 2)
    return entry

def score_all(entries, target_url, target_text, target_keywords):
    scored = []
    for e in entries:
        scored.append(score_entry(e, target_text, target_keywords))

    scored_sorted = sorted(scored, key=lambda x: x["final_score"], reverse=True)

    for idx, s in enumerate(scored_sorted, start=1):
        s["rank"] = idx

    return scored_sorted
