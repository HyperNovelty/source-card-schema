#!/usr/bin/env python3
"""Render a local source card JSON file as static HTML."""

from __future__ import annotations

import html
import sys
from pathlib import Path

try:
    from validate_source_card import ValidationError, load_card, validate_card
except ModuleNotFoundError:
    from scripts.validate_source_card import ValidationError, load_card, validate_card


FIELD_LABELS = [
    ("card_id", "Card ID"),
    ("title", "Title"),
    ("source_type", "Source Type"),
    ("source_locator", "Source Locator"),
    ("captured_at", "Captured At"),
    ("as_of_date", "As Of Date"),
    ("claim_summary", "Claim Summary"),
    ("confidence", "Confidence"),
    ("review_status", "Review Status"),
]

ARRAY_FIELD_LABELS = [
    ("evidence_notes", "Evidence Notes"),
    ("limitations", "Limitations"),
    ("rights_notes", "Rights Notes"),
    ("tags", "Tags"),
]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def render_list(items: list[str]) -> str:
    if not items:
        return "<p class=\"empty\">None recorded.</p>"
    rendered = "\n".join(f"<li>{esc(item)}</li>" for item in items)
    return f"<ul>\n{rendered}\n</ul>"


def render_card_html(card: dict[str, object], warnings: list[str] | None = None) -> str:
    warnings = warnings or []
    title = esc(card["title"])
    status = esc(card["review_status"])

    rows = []
    for field, label in FIELD_LABELS:
        rows.append(
            "<tr>"
            f"<th scope=\"row\">{esc(label)}</th>"
            f"<td>{esc(card[field])}</td>"
            "</tr>"
        )

    sections = []
    for field, label in ARRAY_FIELD_LABELS:
        items = card[field]
        assert isinstance(items, list)
        sections.append(f"<section><h2>{esc(label)}</h2>{render_list(items)}</section>")

    warning_html = ""
    if warnings:
        warning_items = "".join(f"<li>{esc(warning)}</li>" for warning in warnings)
        warning_html = f"<div class=\"warning\"><strong>Warning</strong><ul>{warning_items}</ul></div>"

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Source Card Review - {title}</title>
  <style>
    body {{
      color: #1f2933;
      font-family: Arial, Helvetica, sans-serif;
      line-height: 1.55;
      margin: 0;
      background: #f7f8fa;
    }}
    main {{
      max-width: 920px;
      margin: 0 auto;
      padding: 36px 20px;
      background: #ffffff;
      min-height: 100vh;
    }}
    h1 {{
      color: #111827;
      margin-bottom: 6px;
    }}
    h2 {{
      border-bottom: 1px solid #d8dee6;
      color: #111827;
      font-size: 1.1rem;
      margin-top: 28px;
      padding-bottom: 6px;
    }}
    .meta {{
      color: #4b5563;
      margin-top: 0;
    }}
    table {{
      border-collapse: collapse;
      margin-top: 24px;
      width: 100%;
    }}
    th, td {{
      border: 1px solid #d8dee6;
      padding: 10px;
      text-align: left;
      vertical-align: top;
    }}
    th {{
      background: #eef2f7;
      width: 190px;
    }}
    .warning {{
      background: #fff7ed;
      border: 1px solid #fdba74;
      margin: 18px 0;
      padding: 12px 14px;
    }}
    .empty {{
      color: #6b7280;
      font-style: italic;
    }}
    footer {{
      border-top: 1px solid #d8dee6;
      color: #6b7280;
      font-size: 0.92rem;
      margin-top: 36px;
      padding-top: 16px;
    }}
  </style>
</head>
<body>
  <main>
    <h1>{title}</h1>
    <p class="meta">Local source card review page. Status: <strong>{status}</strong>.</p>
    {warning_html}
    <table>
      <tbody>
        {"".join(rows)}
      </tbody>
    </table>
    {"".join(sections)}
    <footer>
      This page was rendered locally from JSON. The source locator was treated as text and was not fetched or verified.
    </footer>
  </main>
</body>
</html>
"""


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: render_source_card_html.py CARD.json OUT.html", file=sys.stderr)
        return 2

    input_path = Path(argv[1])
    output_path = Path(argv[2])
    try:
        card = load_card(input_path)
        warnings = validate_card(card)
        output_path.write_text(render_card_html(card, warnings), encoding="utf-8")
    except ValidationError as exc:
        print(f"render=failed file={input_path}", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"render=failed output={output_path}", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 1

    for warning in warnings:
        print(warning, file=sys.stderr)
    print(f"render=ok input={input_path} output={output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
