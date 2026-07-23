from __future__ import annotations

from fastapi import FastAPI

from app.schemas.normalization import (
    HealthResponse,
    NormalizeFieldsRequest,
    NormalizeFieldsResponse,
    NormalizeRequest,
    NormalizeResponse,
    normalize_fields_payload,
    normalize_payload,
)

app = FastAPI(
    title="AI Product Matching System",
    description="Backend for the B2B product matching platform.",
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/api/v1/normalize", response_model=NormalizeResponse)
def normalize_text_endpoint(payload: NormalizeRequest) -> NormalizeResponse:
    return normalize_payload(payload)


@app.post("/api/v1/normalize/fields", response_model=NormalizeFieldsResponse)
def normalize_fields_endpoint(payload: NormalizeFieldsRequest) -> NormalizeFieldsResponse:
    return normalize_fields_payload(payload)
