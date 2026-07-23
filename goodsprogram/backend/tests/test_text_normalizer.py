import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.normalization.text_normalizer import build_search_text, normalize_text

client = TestClient(app)


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("Стол детский", "стол детский"),
        ("СТОЛ ДЕТСКИЙ", "стол детский"),
        ("стол   детский", "стол детский"),
        ('"Стол детский"', "стол детский"),
        ("стол—детский", "стол детский"),
        ("стол‑детский", "стол детский"),
        ("ёлка детская", "елка детская"),
        ("1200х600 мм", "1200x600mm"),
        ("1200×600 mm", "1200x600mm"),
        ("220 V", "220v"),
        ("дет. стол", "детский стол"),
        ("д/с стул", "дошкольный стул"),
        ("Стoл детский", "стол детский"),  # Latin o in Cyrillic word
        ("детcкий стол", "детский стол"),  # Latin c in Cyrillic word
        (None, ""),
        ("", ""),
        ("  nan  ", ""),
    ],
)
def test_normalize_text_examples(raw: str | None, expected: str) -> None:
    assert normalize_text(raw) == expected


def test_same_normalized_representation_for_spec_examples() -> None:
    variants = ['"Стол детский"', "СТОЛ ДЕТСКИЙ", "стол   детский"]
    normalized = [normalize_text(value) for value in variants]
    assert len(set(normalized)) == 1
    assert normalized[0] == "стол детский"


def test_build_search_text_skips_empty_fields() -> None:
    assert build_search_text("Стол детский", "", None, "Мебель") == "стол детский мебель"


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_normalize_endpoint() -> None:
    response = client.post("/api/v1/normalize", json={"text": "СТОЛ   ДЕТСКИЙ"})
    assert response.status_code == 200
    assert response.json() == {"normalized": "стол детский"}


def test_normalize_fields_endpoint() -> None:
    response = client.post(
        "/api/v1/normalize/fields",
        json={"fields": ["Стол детский", "1200х600 мм"]},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["normalized_fields"] == ["стол детский", "1200x600mm"]
    assert payload["search_text"] == "стол детский 1200x600mm"
