from __future__ import annotations

from pydantic import BaseModel, Field

from app.normalization.text_normalizer import build_search_text, normalize_text


class NormalizeRequest(BaseModel):
    text: str = Field(..., examples=["Стол   детский"])


class NormalizeResponse(BaseModel):
    normalized: str


class NormalizeFieldsRequest(BaseModel):
    fields: list[str] = Field(
        ...,
        examples=[["Стол детский", "Мебель", "1200х600 мм"]],
    )


class NormalizeFieldsResponse(BaseModel):
    normalized_fields: list[str]
    search_text: str


class HealthResponse(BaseModel):
    status: str


def normalize_payload(payload: NormalizeRequest) -> NormalizeResponse:
    return NormalizeResponse(normalized=normalize_text(payload.text))


def normalize_fields_payload(payload: NormalizeFieldsRequest) -> NormalizeFieldsResponse:
    normalized_fields = [normalize_text(field) for field in payload.fields]
    return NormalizeFieldsResponse(
        normalized_fields=normalized_fields,
        search_text=build_search_text(*payload.fields),
    )
