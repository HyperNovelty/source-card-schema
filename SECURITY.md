# Security Policy

This repo is local-only and stdlib-only. It does not fetch source locators, call external APIs, deploy services, open accounts, or transmit card contents.

## Reporting Issues

For public forks, report security issues through the maintainer channel advertised by that fork. If no channel is listed, open a minimal issue that describes the class of problem without including private data, credentials, source relationships, unpublished material, or sensitive traces.

## Data Boundary

Do not place secrets, credentials, access tokens, account exports, private source relationships, client data, unpublished materials, or sensitive traces in example files, tests, issues, commits, or rendered review pages.

## Local Handling

The scripts read local JSON files and write local HTML files. They treat `source_locator` as plain text and do not attempt network access. Review generated HTML before sharing it, because the rendered page may contain every field from the input card.
