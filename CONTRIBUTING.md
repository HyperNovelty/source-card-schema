# Contributing

Contributions should keep the project local-first, stdlib-only, and public-good oriented.

## Principles

- Preserve provenance without encouraging publication of private traces.
- Keep examples synthetic.
- Avoid hype, authority claims, and compliance claims.
- Do not add external API calls, network fetching, telemetry, account integrations, or publishing features.
- Keep scripts small enough to audit.

## Development

Run the validator, renderer, and unit tests before proposing changes:

```bash
python3 scripts/validate_source_card.py examples/source-card.example.json
python3 scripts/render_source_card_html.py examples/source-card.example.json examples/rendered/source-card.example.html
python3 -m unittest discover -s tests
```

## Documentation

Documentation should describe practical source review habits and clear limits. Do not imply that the schema proves truth, clears rights, supplies legal advice, or replaces expert review.

## Public-Safety Review

Before adding examples or fixtures, check that they do not include private source relationships, credentials, account data, unpublished materials, client details, sensitive traces, or internal project machinery.
