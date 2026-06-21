"""
Vercel serverless function wrapper for FastAPI app.
This allows the FastAPI application to run on Vercel as a serverless function.
"""

import sys
import os

# Add parent directory to Python path so we can import app and services
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import logging

from app.routes.report import router as report_router


def _cors_origins() -> list[str]:
    configured = os.getenv("CORS_ALLOW_ORIGINS", "").strip()
    if configured:
        return [origin.strip() for origin in configured.split(",") if origin.strip()]
    return [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://vercel.app",
    ]


app = FastAPI(
    title="ReportGenie AI",
    description="AI-powered analytics storytelling workspace for CSV business data.",
    version="3.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(report_router)

outputs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
sample_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_data")
os.makedirs(outputs_path, exist_ok=True)

app.mount("/outputs", StaticFiles(directory=outputs_path), name="outputs")
app.mount("/sample_data", StaticFiles(directory=sample_data_path), name="sample_data")

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)


@app.get("/", include_in_schema=False)
def index():
    """Serve frontend for root path (handled by Vercel frontend)"""
    return {"message": "ReportGenie AI Backend", "status": "ok"}


@app.get("/health", include_in_schema=False)
def health():
    """Health check endpoint"""
    return {"status": "healthy"}


# Vercel ASGI adapter
from mangum import Mangum

handler = Mangum(app, lifespan="off")
