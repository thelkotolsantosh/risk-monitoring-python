# Contributing

Contributions are welcome.

## Local setup

```bash
python -m venv .venv
```

Activate the environment and install dependencies:

```bash
pip install -r requirements.txt
```

Run the tests:

```bash
pytest
```

## Guidelines

- Keep the scoring logic explainable.
- Use only synthetic or properly anonymized test data.
- Add tests when adding or changing risk rules.
- Do not commit passwords, API keys, personal data, customer data, or confidential company information.
