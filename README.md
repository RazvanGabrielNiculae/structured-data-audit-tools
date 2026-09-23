# Structured Data Audit Tools

Small, dependency-free validators for auditing JSON-LD against explicit editorial and technical invariants.

This project is intentionally narrower than a general schema generator. It checks whether structured data is parseable, uses expected Schema.org types, and keeps Article identity fields internally coherent. It does **not** claim that passing these checks guarantees Google eligibility, rich results, indexing, ranking, or AI citation.

## Quick start

```bash
python3 tools/audit_jsonld.py examples/article.html --require-type Article
python3 -m unittest discover -s tests -v
```

The command exits non-zero when JSON-LD is missing/malformed, a required type is absent, or an Article-like object lacks core identity fields checked by this tool.

## What it checks

- JSON-LD blocks parse as JSON.
- A requested `@type` exists when `--require-type` is used.
- `Article`, `NewsArticle`, and `BlogPosting` objects include a non-empty `headline`.
- Article-like objects include a usable `author` identity.
- Article-like objects include `datePublished`.
- Multiple JSON-LD blocks and `@graph` containers are traversed.

These are repository QA invariants, not a replacement for current Schema.org or search-platform documentation.

## Source research

The implementation boundary is derived from maintained research at:

- [Structured Data Governance](https://niculae.info/blog/schema-structured-data-governance-retrieve-verify-cite/)
- [Article Schema](https://niculae.info/blog/schema-article-schema-retrieve-verify-cite/)

For the wider SEO/AEO/GEO framework, see [AI Search Frameworks](https://github.com/RazvanGabrielNiculae/ai-search-frameworks).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Keep new checks explicit, testable, and tied to a documented invariant. Avoid encoding volatile platform behavior as an evergreen rule without versioned evidence.
