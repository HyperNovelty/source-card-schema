# Public-Safety Boundary

Source cards are useful because they preserve provenance. They can also create risk if they collect private traces and are later shared without review. This repo is designed for local review and synthetic examples, not for publishing sensitive source material.

## Do Not Include In Public Cards

- Private source relationships.
- Credentials, tokens, passwords, recovery codes, or account identifiers.
- Account exports or client data.
- Unpublished manuscripts, private drafts, internal canon, or restricted materials.
- Sensitive operational traces, private locations, or identifying details that could create personal risk.
- Internal machinery, private workflows, or source relationships that were not meant for public release.

## Before Sharing A Card

Review every field, including tags and rights notes. Confirm that the locator itself does not expose a private path, account, source, or unreleased material. Rendered HTML contains the card contents and should receive the same review as the JSON.

Use `docs/redaction-before-sharing-checklist.md` for a practical redaction pass before any public release.

## What The Tool Cannot Decide

The schema cannot decide whether a claim is true, whether material can be reused, whether publication is safe, or whether a legal or compliance obligation applies. It can only keep review information structured so that humans can make better decisions.
