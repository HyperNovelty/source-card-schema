# Redaction-Before-Sharing Checklist

Use this checklist before sharing a source card JSON file or rendered HTML page. Source cards preserve provenance, so they can expose sensitive relationships and unpublished work if they are copied into public spaces too early.

## Private Relationships

- Remove private source names, source roles, contact details, and relationship hints unless they are explicitly public and approved for this use.
- Check whether tags, evidence notes, or locator text indirectly identify a source.
- Avoid describing why a source had access to material if that relationship is not public.

## Unpublished Or Restricted Work

- Do not include unpublished manuscripts, drafts, internal memos, private research notes, restricted datasets, or embargoed material.
- Replace private document titles with synthetic labels or high-level descriptions when a public demo is needed.
- Confirm the card does not reveal internal review machinery or private project context.

## Paths, Accounts, And Credentials

- Replace local filesystem paths with repo-relative example paths or neutral labels.
- Remove account IDs, console URLs, private workspace names, access tokens, cookies, API keys, passwords, recovery codes, and private keys.
- Treat rendered HTML as a public artifact with the same content risk as the JSON.

## Paid Or Private Data

- Confirm the card does not reproduce paid database content, private exports, licensed data, customer records, client materials, or restricted screenshots.
- Record only public-safe summaries unless the sharing rights are clear.
- Keep private evidence in the trusted workspace rather than embedding it in the public card.

## Quotes And Rights Notes

- Check every quote for length, rights, and context.
- Use short excerpts only when there is a clear reason; otherwise summarize.
- Make rights notes honest about uncertainty instead of implying clearance.

## Dates, As-Of, And Confidence

- Confirm `captured_at` and `as_of_date` are accurate enough for the claim.
- Add limitations when the source may have changed, when the locator was not fetched, or when the card depends on a partial view.
- Keep confidence labels modest and explain important confidence limits in `limitations`.

## Final Pass

- Read every field, including tags and rights notes, as public text.
- If any field requires special trust context to understand safely, keep the card private or rewrite it.
- Share only the smallest useful card for the intended public purpose.
