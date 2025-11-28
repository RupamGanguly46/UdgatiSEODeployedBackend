# master-backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import backend apps
from projectA.main import app as appA
from projectB.main import app as appB
from projectC.main import app as appC

app = FastAPI(title="Master Backend")

# CORS (allow frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # during dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

# MOUNT both backends
app.mount("/projectA", appA)
app.mount("/projectB", appB)
app.mount("/projectC", appC)
