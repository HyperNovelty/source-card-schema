# Source Card Schema

Source Card Schema is a local-first starter repo for creating durable source cards from links, documents, claims, and signals. A source card is a small JSON record that preserves what was captured, when it was captured, what claim it supports or questions, what limitations are known, and what review state the card is in.

The goal is practical provenance. The repo is meant to help researchers, educators, journalists, analysts, librarians, civic groups, and small teams keep source notes structured without publishing private traces or depending on a hosted service.

This is repo candidate #8 in the Hypernovelty Open Lab footprint.

## What This Provides

- A simple JSON Schema for source cards.
- Synthetic example cards.
- A stdlib-only validator with a few project rules.
- A stdlib-only HTML renderer for local review pages.
- Field guidance and public-safety boundaries.

## What A Source Card Is

A source card is not a final article, fact-check, legal memo, or citation manager export. It is a compact review object that records:

- the source type and locator as text,
- the capture and as-of dates,
- a short claim summary,
- evidence notes and limitations,
- rights notes,
- review status,
- tags for later sorting.

The `source_locator` field may contain a URL, file name, archive reference, accession number, interview note label, or other locator text. This repo never fetches or verifies that locator.

## Who It Helps

Source cards can help:

- researchers preserve provenance during early discovery,
- educators teach source review and evidence limits,
- journalists and analysts separate claims from notes,
- small teams keep review status visible,
- public-interest projects avoid mixing private traces into public artifacts.

## Quick Start

Validate the full synthetic example:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_source_card.py examples/source-card.example.json
```

Validate the minimal synthetic example:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_source_card.py examples/source-card-minimal.example.json
```

Render a checked-in demo HTML review page:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/render_source_card_html.py examples/source-card.example.json examples/rendered/source-card.example.html
```

Open `examples/rendered/source-card.example.html` in a browser. The rendered page is static HTML and should open on Windows, macOS, or Linux.

Run the tests:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
```

## Review Status

Allowed `review_status` values are:

- `draft`
- `reviewed`
- `needs_followup`
- `do_not_publish`

If a card is marked `reviewed`, it must include at least one `evidence_notes` entry. If a card is marked `do_not_publish`, validation can still pass, but the validator prints a visible warning.

## What This Repo Does Not Do

This repo does not:

- fetch, crawl, scrape, archive, or open `source_locator`,
- verify whether a claim is true,
- act as a fact-checking authority,
- provide legal, compliance, financial, medical, or safety advice,
- clear rights or determine publication permission,
- replace direct source review,
- manage accounts, credentials, private notebooks, or publishing workflows,
- publish, sync, deploy, or call external APIs.

## Public-Safety Boundary

Do not put private source relationships, credentials, account data, unpublished or private materials, sensitive traces, client data, internal machinery, or personal-risk details into source cards intended for public release.

Use synthetic examples for demos. For real work, maintain a separate redaction and publication review process before sharing any card outside the trusted context where it was created.

## Repository Layout

```text
README.md
START_HERE.html
docs/field-guide.md
docs/public-safety-boundary.md
schemas/source-card.schema.json
examples/source-card.example.json
examples/source-card-minimal.example.json
scripts/validate_source_card.py
scripts/render_source_card_html.py
tests/
```

## Open Lab Fit

This repo is part of the Hypernovelty Open Lab public proof footprint. See `docs/open-lab-positioning.md` for how source cards support agent receipts, workflow screens, verification literacy labs, school readiness review, and the umbrella survival kit.

## License

Released under the MIT License. See `LICENSE`.
