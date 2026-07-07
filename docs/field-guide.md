# Source Card Field Guide

This guide explains how to fill out a source card in a practical, public-safe way. The format is intentionally small so that cards can be reviewed in plain text, versioned, and rendered as local HTML.

## Fields

`card_id`: A stable local identifier. Use a short slug or structured ID that does not expose private relationships.

`title`: A plain-language title for the card. Prefer descriptive titles over conclusions.

`source_type`: The kind of source being described, such as `article`, `report`, `dataset`, `interview_note`, `public_record`, `webpage`, or `observation`.

`source_locator`: Locator text only. This may be a URL, archive label, report title, file label, or accession reference. The validator and renderer do not fetch it.

`captured_at`: Date or timestamp for when the source or signal was captured.

`as_of_date`: Date the source card should be understood against. Use this to make stale or time-sensitive claims easier to review later.

`claim_summary`: Short summary of the claim, signal, or observation being preserved. Keep it separate from evidence notes.

`evidence_notes`: Array of short notes describing what the source appears to support. A reviewed card must include at least one evidence note.

`confidence`: A plain-language confidence label, such as `low`, `medium`, `high`, or a local review phrase.

`limitations`: Array of known limits, missing context, uncertainty, or reasons the card should not be overread.

`rights_notes`: Array of notes about reuse, quotation, licensing, access restrictions, or publication uncertainty. These notes do not clear rights.

`review_status`: One of `draft`, `reviewed`, `needs_followup`, or `do_not_publish`.

`tags`: Array of public-safe tags for grouping and retrieval.

## Review Practice

Keep claim language modest. A source card records provenance and review state; it does not prove truth by itself. Use `limitations` generously when the source is incomplete, stale, contested, machine-generated, or outside your expertise.

Use `do_not_publish` for cards that are valid for internal tracking but should not leave the local review context. The validator will pass those cards and print a warning.
