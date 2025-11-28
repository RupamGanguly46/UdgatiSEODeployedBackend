# from fastapi import FastAPI
# from pydantic import BaseModel
# from agents import run_seo_chain

# app = FastAPI()

# class SEORequest(BaseModel):
#     text: str

# @app.post("/run_chain")
# def run_chain_api(req: SEORequest):
#     result = run_seo_chain(req.text)
#     return result

from fastapi import FastAPI
from pydantic import BaseModel
from projectC.agents import run_seo_chain
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ------------------------------
# ENABLE CORS FOR FRONTEND
# ------------------------------
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],      # Allow all frontend URLs
#     allow_credentials=True,
#     allow_methods=["*"],      # VERY IMPORTANT (allows OPTIONS)
#     allow_headers=["*"],
# )

# ------------------------------
# API MODEL
# ------------------------------
class SEORequest(BaseModel):
    text: str

# ------------------------------
# API ROUTE
# ------------------------------
@app.post("/run_chain")
def run_chain_api(req: SEORequest):
    return run_seo_chain(req.text)

