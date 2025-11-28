
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from projectA.pipeline.pipeline import run_analysis
import asyncio

app = FastAPI(title="Simple SEO Competitor Analysis")

@app.get("/analyze")
async def analyze(url: str):
    try:
        result = await run_analysis(url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
