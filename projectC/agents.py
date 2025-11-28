from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

# ------------------------------
# LLM CLIENT (Azure OpenAI)
# ------------------------------
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)

# ------------------------------
# AGENT 1 — Extract Topic
# ------------------------------
def agent_extract_topic(text: str):
    prompt = f"""
    You are an advanced SEO topic extraction and optimization agent.

    TASKS:
    1. Extract the TRUE original topic from the user's text.
    2. Optimize that topic into a short (2–6 word), rankable SEO topic:
       - High search intent
       - Commercially valuable
       - Search-friendly phrasing
       - Google-optimized

    OUTPUT FORMAT (strict):
    Original Topic: <extracted topic>
    Optimized Topic: <optimized SEO topic>

    RULES:
    - No explanations
    - No extra text
    - No lists or paragraphs
    - Do NOT add quotes

    USER TEXT:
    {text}
    """
    result = llm.invoke([HumanMessage(content=prompt)])
    return result.content.strip()


# ------------------------------
# AGENT 2 — Generate Keywords
# ------------------------------
def agent_generate_keywords(topic: str):
    prompt = f"""
    You are an advanced SEO keyword generation agent.

    GOAL:
    Generate EXACTLY 10 high-performing SEO keywords that are:
    - Highly relevant to the topic
    - Semantically related to typical website content on this subject
    - Optimized for search engines (Google SEO best practices)
    - A mix of: 
        * 3 primary keywords (high-volume)
        * 4 secondary keywords (supporting relevance)
        * 3 long-tail, high-intent keywords (lower competition)

    CONTEXT:
    These keywords will be used by a website to improve ranking, 
    so they must reflect what users actually search for online.

    RULES:
    - Output MUST be a single comma-separated list.
    - NO numbering.
    - NO explanations.
    - NO additional text.
    - Each keyword must be natural and search-friendly.

    TOPIC: {topic}
    """
    result = llm.invoke([HumanMessage(content=prompt)])
    return result.content.strip()


# ------------------------------
# AGENT 3 — SEO Writer
# ------------------------------
def agent_write_seo(topic: str, keywords: str):
    prompt = f"""
    You are an enterprise-grade SEO metadata optimization agent.

    OBJECTIVE:
    Using the provided topic and keywords, generate ALL essential SEO meta tags
    required for strong SERP performance, high CTR, and proper social-sharing previews.

    INCLUDE:
    1. SEO Title (max 60 characters, high CTR, includes 1 primary keyword)
    2. Meta Description (max 155 characters, high-intent, includes 1–2 keywords)
    3. Meta Keywords (comma-separated, refined version of provided keywords)
    4. Canonical URL Slug (SEO-friendly, lowercase, hyphens, no stopwords)
    5. Open Graph Title (engaging, share-worthy)
    6. Open Graph Description (short, compelling, 120–140 chars)
    7. Suggested H1 Heading (semantic and intent-aligned)

    RULES:
    - Use natural language; no keyword stuffing.
    - Do NOT add explanations or notes.
    - ONLY output in the following EXACT structured format:

    Title: <title>
    Meta Description: <meta description>
    Meta Keywords: <meta keywords>
    Slug: <url-slug>
    OG Title: <og title>
    OG Description: <og description>
    H1: <h1 heading>

    INPUT TOPIC:
    {topic}

    INPUT KEYWORDS:
    {keywords}
    """
    result = llm.invoke([HumanMessage(content=prompt)])
    return result.content.strip()


# ------------------------------------------
# AGENT 4 — SEO Blog Outline Generator
# ------------------------------------------
def agent_generate_outline(topic: str, keywords: str):
    prompt = f"""
    You are an advanced SEO content outline generator.

    GOAL:
    Create a full SEO-friendly blog outline using:
    - The optimized topic
    - The keyword list
    - Google EEAT + search intent best practices

    OUTPUT MUST INCLUDE:
    - H1
    - 4–6 H2 sections
    - 2–3 H3 subsections under each H2
    - A FAQ section with 4 questions

    RULES:
    - Do NOT write full paragraphs.
    - Only headings and bullet points.
    - No extra explanation.

    TOPIC:
    {topic}

    KEYWORDS:
    {keywords}
    """
    result = llm.invoke([HumanMessage(content=prompt)])
    return result.content.strip()


# # ------------------------------
# # THE CHAIN (Agent → Agent → Agent)
# # ------------------------------
# def run_seo_chain(user_text: str):
#     topic = agent_extract_topic(user_text)
#     keywords = agent_generate_keywords(topic)
#     seo_output = agent_write_seo(topic, keywords)

#     return {
#         "topic": topic,
#         "keywords": keywords,
#         "final_output": seo_output
#     }

# ------------------------------------------
# THE MAIN SEO CHAIN
# ------------------------------------------
def run_seo_chain(user_text: str):
    # Step 1: Extract and optimize topic
    topic_output = agent_extract_topic(user_text)

    # Parse the optimized topic line
    optimized_topic = ""
    for line in topic_output.split("\n"):
        if line.lower().startswith("optimized topic:"):
            optimized_topic = line.split(":", 1)[1].strip()

    # Step 2: Generate SEO keywords
    keywords_output = agent_generate_keywords(optimized_topic)

    # Step 3: Generate full SEO meta tags
    meta_output = agent_write_seo(optimized_topic, keywords_output)

    # Step 4: Generate SEO blog outline
    outline_output = agent_generate_outline(optimized_topic, keywords_output)

    return {
        "topic_details": topic_output,
        "optimized_topic": optimized_topic,
        "keywords": keywords_output,
        "meta_tags": meta_output,
        "outline": outline_output
    }
