# Contributing

Languages: [繁體中文](../CONTRIBUTING.md) · [English (UK)](CONTRIBUTING.en-GB.md)

This is a course-project public-opinion platform for Uma Musume. Fixes, docs, and tidy-ups are welcome — match the current tree before you start.

## Before you edit

1. Read [`.cursorrules`](../.cursorrules) and [`AGENTS.md`](../AGENTS.md).
2. If architecture, flow, the data contract, or routes change, open the matching file in [`SPEC/`](../SPEC/INTENT_SPEC.md).
3. When spec and code disagree, **the code wins**, then the spec is corrected.

## Conventions

| Item | Rule |
| --- | --- |
| Comments and maintainer errors | Traditional Chinese; avoid Simplified Chinese and PRC wording |
| Variables / functions | `snake_case` |
| Classes | `PascalCase` |
| Route paths | kebab-case (`/crawler-admin/`, no underscores) |
| Date / time | `YYYY-MM-DD`, `HH:MM:SS`, Asia/Taipei |
| In-site URLs | `{% url %}` in templates; `reverse()` / `reverse_lazy()` in Python |
| Write AJAX | Send `X-CSRFToken`; handle `error` / `catch` |
| Model changes | Always ship a migration |
| `data/raw`, `data/processed` | Do not casually rename or reorder core columns |

## Please do not

- Hard-code keys, tokens, passwords, or absolute machine paths
- Commit `.env`, credentials, `db.sqlite3`, or bulky `media/`
- Change a model without a migration
- Flatten `app_*` packages back onto the repository root (the map is `website_configs/app_layout.py`)

Ask first for irreversible work (dropping databases, `compose down -v`, force-push, expensive bulk LLM calls).

## After a change

1. Contract or routes changed → update `SPEC/`
2. Record the change in [`CHANGELOG.md`](../CHANGELOG.md): purpose, scope, how to verify; **do not reuse a version number**
3. New or changed APIs: route resolves, errors are readable, the happy path can be reproduced
4. UI changes: walk the flow in a browser (a single screenshot is not verification)

User-facing copy lives in [`README.md`](../README.md) (Traditional Chinese) and [`README.en-GB.md`](./README.en-GB.md) (British English). Install and architecture are split under `docs/`.
