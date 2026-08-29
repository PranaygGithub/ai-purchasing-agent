from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from .models import Scenario1Request, Scenario2Request
from .agent import analyze_scenario1, analyze_scenario2

app = FastAPI(
    title="Procura AI — Purchasing Agent",
    description="AI Purchasing Agent assignment implementation for scenarios 1 and 2.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
def health():
    return {"status": "ok", "service": "Procura AI Purchasing Agent"}


@app.post("/api/scenario1/analyze")
def scenario1(request: Scenario1Request):
    return analyze_scenario1(request)


@app.post("/api/scenario2/analyze")
def scenario2(request: Scenario2Request):
    return analyze_scenario2(request)


@app.get("/styles.css", include_in_schema=False)
def styles():
    return FileResponse(FRONTEND_DIR / "style.css", media_type="text/css")


@app.get("/app.js", include_in_schema=False)
def javascript():
    return FileResponse(FRONTEND_DIR / "app.js", media_type="application/javascript")
