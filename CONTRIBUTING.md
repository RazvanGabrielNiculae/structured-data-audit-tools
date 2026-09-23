# Contributing

1. Add a positive or negative fixture for every new rule.
2. Keep the standard-library-only runtime unless a dependency has a demonstrated need.
3. Separate Schema.org vocabulary checks from search-platform eligibility claims.
4. Never include credentials, private data, or proprietary page content in fixtures.
5. Run `python3 -m unittest discover -s tests -v` before opening a pull request.
