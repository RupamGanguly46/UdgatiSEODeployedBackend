# import asyncio
# from .fetch import fetch_page
# from .keywords import extract_keywords
# from .competitors import find_competitors
# from .scoring import score_all

# async def analyze_single(url, target_text, target_keywords):
#     html, text = await fetch_page(url)
#     return {'url': url, 'html': html, 'text': text}

# async def run_analysis(target_url):
#     # Fetch target
#     target_html, target_text = await fetch_page(target_url)
#     target_keywords = extract_keywords(target_text)

#     # Find competitors
#     candidates = await find_competitors(target_keywords, max_candidates=10)
#     # ensure target isn't in candidates
#     candidates = [c for c in candidates if c and target_url not in c]
#     # Add target as first to score itself
#     to_fetch = [target_url] + candidates

#     # Fetch pages in parallel
#     tasks = [analyze_single(u, target_text, target_keywords) for u in to_fetch]
#     results = await asyncio.gather(*tasks)

#     # Score everything
#     scored = score_all(results, target_url, target_text, target_keywords)
#     # Build response: find top5 competitors (exclude target)
#     target_entry = next((s for s in scored if s['url'] == target_url), None)
#     competitors = [s for s in scored if s['url'] != target_url][:5]
#     return {
#         'target': target_entry,
#         'competitors': competitors,
#         'all': scored
#     }

import asyncio
from .fetch import fetch_page
from .keywords import extract_keywords
from .competitors import find_competitors
from .scoring import score_all

async def analyze_single(url, target_text, target_keywords):
    html, text = await fetch_page(url)
    return {'url': url, 'html': html, 'text': text}

async def run_analysis(target_url):
    # Fetch the target website
    target_html, target_text = await fetch_page(target_url)
    target_keywords = extract_keywords(target_text)

    # Get competitor candidate URLs
    candidates = await find_competitors(target_keywords, max_candidates=10)

    # Prevent duplicates
    candidates = [c for c in candidates if c and target_url not in c]

    # We fetch both target + competitors in parallel
    to_fetch = [target_url] + candidates

    tasks = [analyze_single(u, target_text, target_keywords) for u in to_fetch]
    results = await asyncio.gather(*tasks)

    # IMPORTANT: skip some metrics for the target website
    for r in results:
        if r['url'] == target_url:
            # Mark that these metrics cannot be computed for the target
            r['_is_target'] = True
            r['_skip_metrics'] = ['content_similarity', 'engagement']
        else:
            r['_is_target'] = False
            r['_skip_metrics'] = []

    # Compute scores for target + competitor sites
    scored = score_all(results, target_url, target_text, target_keywords)

    # Extract target + top 5 competitors
    target_entry = next((s for s in scored if s['url'] == target_url), None)
    competitors = [s for s in scored if s['url'] != target_url][:5]

    return {
        'target': target_entry,
        'competitors': competitors,
        'all': scored
    }
