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
    return f"<ul class=\"check-list\">\n{rendered}\n</ul>"


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
    warning_block = f"    {warning_html}\n" if warning_html else ""

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Source Card Review - {title}</title>
  <style>
    :root {{ color-scheme: dark; --ink: #f7ead7; --muted: #d7c2a2; --paper: #fff7e8; --paper-ink: #261b12; --line: #6f5840; --accent: #f2b66d; --warn: #ffd08a; }}
    * {{ box-sizing: border-box; }}
    body {{ color: var(--ink); font-family: Georgia, "Times New Roman", serif; line-height: 1.6; margin: 0; background: #20150f; }}
    body::before {{ content: ""; position: fixed; inset: 0; pointer-events: none; background: radial-gradient(circle at top left, rgba(242, 182, 109, 0.16), transparent 34rem); }}
    main {{ max-width: 1080px; margin: 0 auto; padding: 32px 18px 44px; position: relative; }}
    header {{ border: 1px solid var(--line); border-radius: 8px; margin-bottom: 18px; padding: 24px; background: linear-gradient(135deg, #3a2617, #251810); box-shadow: 0 18px 50px rgba(0,0,0,0.25); }}
    h1 {{ color: var(--ink); font-size: clamp(2rem, 5vw, 4rem); line-height: 0.98; margin: 10px 0 14px; letter-spacing: 0; }}
    h2 {{ color: var(--paper-ink); font-size: 1.02rem; line-height: 1.2; margin: 0 0 10px; }}
    p {{ margin: 0; }}
    section, .table-card {{ background: var(--paper); border: 1px solid #dfcaa8; border-radius: 8px; color: var(--paper-ink); padding: 18px; }}
    .eyebrow {{ color: var(--accent); font-family: Arial, Helvetica, sans-serif; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }}
    .meta {{ color: var(--muted); margin: 0 0 14px; }}
    .chips {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .chip {{ border: 1px solid rgba(255,255,255,0.28); border-radius: 999px; color: var(--ink); display: inline-flex; font-family: Arial, Helvetica, sans-serif; font-size: 0.78rem; font-weight: 700; padding: 6px 10px; }}
    .chip.warn {{ background: rgba(255, 208, 138, 0.18); color: #ffe2ac; }}
    .chip.neutral {{ background: rgba(255,255,255,0.08); }}
    .section-grid {{ display: grid; gap: 14px; grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    .table-card {{ margin-bottom: 14px; overflow-x: auto; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border-bottom: 1px solid #dfcaa8; padding: 10px 8px; text-align: left; vertical-align: top; }}
    tr:last-child th, tr:last-child td {{ border-bottom: 0; }}
    th {{ color: #735230; font-family: Arial, Helvetica, sans-serif; font-size: 0.75rem; text-transform: uppercase; width: 190px; }}
    .warning {{ background: #fff1d6; border: 1px solid #d99745; border-radius: 8px; color: var(--paper-ink); margin: 18px 0; padding: 12px 14px; }}
    .check-list {{ margin: 0; padding-left: 1.2rem; }}
    .check-list li {{ margin: 0.45rem 0; padding-left: 0.15rem; }}
    .empty {{ color: #7a6a55; font-style: italic; }}
    footer {{ color: var(--muted); font-family: Arial, Helvetica, sans-serif; font-size: 0.9rem; margin-top: 18px; }}
    @media (max-width: 760px) {{ .section-grid {{ grid-template-columns: 1fr; }} header {{ padding: 20px; }} th {{ width: 150px; }} }}
    @media print {{ body {{ background: #fff; color: #000; }} body::before {{ display: none; }} main {{ max-width: none; padding: 0; }} header, section, .table-card {{ box-shadow: none; break-inside: avoid; }} }}
  </style>
</head>
<body>
  <main>
    <header>
      <p class="eyebrow">Hypernovelty Open Lab / Source Card</p>
      <h1>{title}</h1>
      <p class="meta">Local source card review page for synthetic/example source documentation.</p>
      <div class="chips" aria-label="Source card status">
        <span class="chip warn">Review status: {status}</span>
        <span class="chip neutral">Confidence: {esc(card["confidence"])}</span>
        <span class="chip neutral">Source not fetched</span>
      </div>
    </header>
{warning_block}    <section class="table-card" aria-labelledby="summary-heading">
      <h2 id="summary-heading">Summary Metadata</h2>
      <table>
      <tbody>
        {"".join(rows)}
      </tbody>
      </table>
    </section>
    <div class="section-grid">{"".join(sections)}</div>
    <footer>
      This page was rendered locally from JSON. The source locator was treated as text and was not fetched or verified; this is not a rights determination, publication approval, or factual certification.
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
