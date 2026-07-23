"""
Text normalization pipeline (B2B spec §6).

Turns raw product text into a canonical form so that variants like
"Стол детский", "СТОЛ ДЕТСКИЙ", and "стол   детский" collapse to
the same normalized representation.
"""

from __future__ import annotations

import re
import unicodedata

from app.normalization.abbreviations import ABBREVIATIONS

# Latin letters that visually match Cyrillic counterparts in procurement data.
_LATIN_TO_CYRILLIC = str.maketrans(
    {
        "a": "а",
        "A": "а",
        "b": "в",  # rare; "B" often typed instead of "В"
        "B": "в",
        "c": "с",
        "C": "с",
        "e": "е",
        "E": "е",
        "h": "н",
        "H": "н",
        "k": "к",
        "K": "к",
        "m": "м",
        "M": "м",
        "o": "о",
        "O": "о",
        "p": "р",
        "P": "р",
        "t": "т",
        "T": "т",
        "y": "у",
        "Y": "у",
    }
)

# Dimension separator: Cyrillic х and multiplication sign → latin x.
_DIMENSION_SEPARATOR_RE = re.compile(r"(\d)\s*[xх×X]\s*(\d)", re.UNICODE)

_QUOTE_CHARS = "\"'`´''""«»„“”‚‘’"
_HYPHEN_CHARS = "-–—―‑‒−"

# Punctuation kept as word boundaries; everything else becomes a space.
_PUNCTUATION_RE = re.compile(r"[^\w\s]", re.UNICODE)
_WHITESPACE_RE = re.compile(r"\s+")

# "<number> <unit>" → "<number><unit>" for common procurement units.
_UNIT_SPACING_RE = re.compile(
    r"(\d+(?:[.,]\d+)?)\s*[-]?\s*(mm|cm|m|kg|g|ml|l|w|v|a|hz|kw|kwt|vt|шт)\b",
    re.IGNORECASE,
)

_UNIT_WORDS: list[tuple[str, str]] = [
    (r"\bmillimeters?\b", "mm"),
    (r"\bmillimetres?\b", "mm"),
    (r"\bмиллиметр(?:ов|а)?\b", "mm"),
    (r"\bмм\b", "mm"),
    (r"\bcentimeters?\b", "cm"),
    (r"\bcentimetres?\b", "cm"),
    (r"\bсантиметр(?:ов|а)?\b", "cm"),
    (r"\bсм\b", "cm"),
    (r"\bmeters?\b", "m"),
    (r"\bmetres?\b", "m"),
    (r"\bметр(?:ов|а)?\b", "m"),
    (r"\bkilograms?\b", "kg"),
    (r"\bкилограмм(?:ов|а)?\b", "kg"),
    (r"\bкг\b", "kg"),
    (r"\bgrams?\b", "g"),
    (r"\bграмм(?:ов|а)?\b", "g"),
    (r"\bliters?\b", "l"),
    (r"\blitres?\b", "l"),
    (r"\bлитр(?:ов|а)?\b", "l"),
    (r"\bmilliliters?\b", "ml"),
    (r"\bmillilitres?\b", "ml"),
    (r"\bмиллилитр(?:ов|а)?\b", "ml"),
    (r"\bwatts?\b", "w"),
    (r"\bватт(?:ов|а)?\b", "w"),
    (r"\bvolts?\b", "v"),
    (r"\bвольт(?:ов|а)?\b", "v"),
    (r"\bamperes?\b", "a"),
    (r"\bампер(?:ов|а)?\b", "a"),
    (r"\bhertz\b", "hz"),
    (r"\bгерц\b", "hz"),
    (r"\bштук(?:а|и)?\b", "шт"),
    (r"\bшт\b", "шт"),
]


def _coerce_input(text: str | None) -> str:
    if text is None:
        return ""
    text = str(text).strip()
    if text.lower() in {"nan", "none", "null"}:
        return ""
    return text


def _unicode_normalize(text: str) -> str:
    return unicodedata.normalize("NFKC", text)


def _normalize_yo(text: str) -> str:
    return text.replace("ё", "е").replace("Ё", "е")


def _normalize_homoglyphs(text: str) -> str:
    text = text.translate(_LATIN_TO_CYRILLIC)
    return _DIMENSION_SEPARATOR_RE.sub(r"\1x\2", text)


def _normalize_quotes(text: str) -> str:
    for char in _QUOTE_CHARS:
        text = text.replace(char, " ")
    return text


def _normalize_hyphens(text: str) -> str:
    for char in _HYPHEN_CHARS:
        text = text.replace(char, "-")
    # Hyphenated words become spaced tokens for matching.
    text = re.sub(r"(?<=\w)-(?=\w)", " ", text)
    text = text.replace("-", " ")
    return text


def _standardize_units(text: str) -> str:
    for pattern, replacement in _UNIT_WORDS:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    text = _UNIT_SPACING_RE.sub(
        lambda m: f"{m.group(1).replace(',', '.')}{m.group(2).lower()}",
        text,
    )
    return text


def _expand_abbreviations(text: str) -> str:
    lowered = text.lower()
    for key in sorted(ABBREVIATIONS, key=len, reverse=True):
        pattern = rf"(?<![\w/]){re.escape(key)}(?![\w/])"
        lowered = re.sub(pattern, ABBREVIATIONS[key], lowered)
    return lowered


def _normalize_punctuation(text: str) -> str:
    return _PUNCTUATION_RE.sub(" ", text)


def _collapse_whitespace(text: str) -> str:
    return _WHITESPACE_RE.sub(" ", text).strip()


def normalize_text(text: str | None) -> str:
    """Apply the full §6 text normalization pipeline to a single field."""
    text = _coerce_input(text)
    if not text:
        return ""

    text = _unicode_normalize(text)
    text = text.lower()
    text = _normalize_homoglyphs(text)
    text = _normalize_yo(text)
    text = _normalize_quotes(text)
    text = _normalize_hyphens(text)
    text = _expand_abbreviations(text)
    text = _standardize_units(text)
    text = _normalize_punctuation(text)
    text = _collapse_whitespace(text)
    return text


def normalize_product_name(product_name: str | None) -> str:
    """Normalized name used for exact match and search indexing."""
    return normalize_text(product_name)


def build_search_text(*fields: str | None) -> str:
    """Join normalized product fields into one searchable blob."""
    parts = [normalize_text(field) for field in fields if _coerce_input(field)]
    return _collapse_whitespace(" ".join(parts))
