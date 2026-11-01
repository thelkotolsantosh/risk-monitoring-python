# Risk Monitoring in Python

A simple transaction risk-monitoring project built with Python.

The project generates synthetic transaction data, applies a set of configurable risk rules, assigns a risk score to each transaction, and creates alerts for transactions that may require review.

I built this project to explore how rule-based transaction monitoring can be implemented in Python while keeping the scoring logic easy to understand and modify.

## What it does

The workflow is straightforward:

```text
Synthetic transactions
        ↓
Data validation
        ↓
Risk rules
        ↓
Risk score
        ↓
Risk classification
        ↓
Alerts and reports
```

The project checks transactions for signals such as:

- unusually high transaction amounts
- high customer/KYC risk
- repeated failed logins
- previous chargebacks
- large changes in IP location
- new payees
- high transaction frequency
- recently created accounts

Each triggered rule adds points to the transaction's risk score.

## Risk levels

| Score | Level |
|---:|---|
| 0–24 | Low |
| 25–49 | Medium |
| 50–74 | High |
| 75+ | Critical |

The scoring thresholds and rule weights can be changed in:

```text
config/risk_rules.json
```

This keeps the risk logic configurable instead of hard-coding every value in the Python scripts.

## Project structure

```text
risk-monitoring-python/
│
├── config/
│   └── risk_rules.json
│
├── data/
│   └── README.md
│
├── outputs/
│
├── src/
│   ├── __init__.py
│   ├── generate_data.py
│   ├── main.py
│   └── risk_engine.py
│
├── tests/
│   └── test_risk_engine.py
│
├── dashboard.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

Clone the repository:

```bash
git clone https://github.com/thelkotolsantosh/risk-monitoring-python-.git
cd risk-monitoring-python-
```

Create a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Generate sample data

Run:

```bash
python -m src.generate_data
```

This generates a synthetic transaction dataset at:

```text
data/transactions.csv
```

The dataset contains fields such as transaction amount, customer risk level, failed login attempts, transaction frequency, account age, country, and payee status.

No real customer or financial data is used.

## Run the risk monitor

```bash
python -m src.main
```

The script scores each transaction and creates:

```text
outputs/scored_transactions.csv
outputs/risk_alerts.csv
outputs/risk_summary.csv
```

### Example

A transaction could trigger:

```text
Amount: 42,000
KYC Risk: High
New Payee: Yes
```

and produce:

```text
Risk Score: 55
Risk Level: High

Reasons:
High transaction amount
High KYC risk
New payee
```

I included the reasons behind each score so that flagged transactions are explainable rather than just returning a number.

## Dashboard

The project also includes a small Streamlit dashboard.

Start it with:

```bash
streamlit run dashboard.py
```

The dashboard shows:

- number of transactions processed
- High and Critical alerts
- risk-level distribution
- highest-scoring transactions
- risk levels by transaction channel

## Tests

Run the tests with:

```bash
pytest
```

The tests cover the main scoring and classification logic.

## Tools used

- Python
- Pandas
- NumPy
- Streamlit
- Pytest

## Note

This is a learning project built with synthetic data. The rules and thresholds are simplified for demonstration purposes and should not be treated as a production fraud, AML, KYC, or financial-risk decisioning system.

---

**Santosh Thelkotlol**

[GitHub Profile](https://github.com/thelkotolsantosh)
