#!/usr/bin/env python3
"""Validate a local source card JSON file.

This validator intentionally does not fetch, open, or verify source_locator.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_STRING_FIELDS = [
    "card_id",
    "title",
    "source_type",
    "source_locator",
    "captured_at",
    "as_of_date",
    "claim_summary",
    "confidence",
    "review_status",
]

REQUIRED_ARRAY_FIELDS = [
    "evidence_notes",
    "limitations",
    "rights_notes",
    "tags",
]

REQUIRED_FIELDS = REQUIRED_STRING_FIELDS + REQUIRED_ARRAY_FIELDS
ALLOWED_REVIEW_STATUS = {"draft", "reviewed", "needs_followup", "do_not_publish"}


class ValidationError(Exception):
    """Raised when a source card fails validation."""


def load_card(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON: {exc}") from exc
    except OSError as exc:
        raise ValidationError(f"could not read file: {exc}") from exc

    if not isinstance(data, dict):
        raise ValidationError("card must be a JSON object")
    return data


def validate_card(card: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    warnings: list[str] = []

    for field in REQUIRED_FIELDS:
        if field not in card:
            errors.append(f"missing required field: {field}")

    allowed_fields = set(REQUIRED_FIELDS)
    for field in sorted(set(card) - allowed_fields):
        errors.append(f"unexpected field: {field}")

    for field in REQUIRED_STRING_FIELDS:
        value = card.get(field)
        if field in card and not isinstance(value, str):
            errors.append(f"{field} must be a string")
        elif isinstance(value, str) and not value.strip():
            errors.append(f"{field} must not be empty")

    for field in REQUIRED_ARRAY_FIELDS:
        value = card.get(field)
        if field in card and not isinstance(value, list):
            errors.append(f"{field} must be an array of strings")
            continue
        if isinstance(value, list):
            for index, item in enumerate(value):
                if not isinstance(item, str):
                    errors.append(f"{field}[{index}] must be a string")

    review_status = card.get("review_status")
    if isinstance(review_status, str) and review_status not in ALLOWED_REVIEW_STATUS:
        allowed = ", ".join(sorted(ALLOWED_REVIEW_STATUS))
        errors.append(f"review_status must be one of: {allowed}")

    evidence_notes = card.get("evidence_notes")
    if review_status == "reviewed" and isinstance(evidence_notes, list) and not evidence_notes:
        errors.append("reviewed cards must include at least one evidence_notes entry")

    if review_status == "do_not_publish":
        warnings.append("WARNING: review_status is do_not_publish; do not publish this card.")

    if errors:
        raise ValidationError("\n".join(errors))
    return warnings


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_source_card.py CARD.json", file=sys.stderr)
        return 2

    path = Path(argv[1])
    try:
        warnings = validate_card(load_card(path))
    except ValidationError as exc:
        print(f"validation=failed file={path}", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 1

    for warning in warnings:
        print(warning, file=sys.stderr)
    print(f"validation=ok file={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
