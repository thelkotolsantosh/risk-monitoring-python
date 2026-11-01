# Risk Monitoring Project in Python

A portfolio-ready **risk monitoring and transaction alerting project** built with Python and fully synthetic data.

The project simulates a simplified fraud / operational-risk monitoring workflow:

1. Generate fake transaction and customer-risk data.
2. Apply transparent, rule-based risk scoring.
3. Assign Low, Medium, High, or Critical risk levels.
4. Record the reasons that caused each alert.
5. Export alerts for investigation.
6. Review results in a Streamlit dashboard.
7. Run automated tests through GitHub Actions.

> **Important:** This repository uses synthetic data only. It is an educational portfolio project and is not a production fraud-detection, AML, KYC, or regulatory compliance system.

## Why this project is useful

This project demonstrates practical skills in:

- Python
- Pandas
- NumPy
- Risk monitoring
- Rule-based alert generation
- Transaction monitoring
- Data analysis
- Data quality checks
- Explainable risk scoring
- CSV reporting
- Streamlit dashboards
- Unit testing with pytest
- Git / GitHub
- GitHub Actions CI

## Project structure

```text
risk-monitoring-python/
├── .github/
│   └── workflows/
│       └── python-tests.yml
├── config/
│   └── risk_rules.json
├── data/
│   └── README.md
├── outputs/
│   └── .gitkeep
├── src/
│   ├── __init__.py
│   ├── generate_data.py
│   ├── main.py
│   └── risk_engine.py
├── tests/
│   └── test_risk_engine.py
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── requirements.txt
```

## Risk model

The model is intentionally simple and explainable.

Example risk signals include:

- High transaction amount
- High KYC/customer-risk level
- Multiple failed logins
- Previous chargebacks
- Large IP-location change
- New payee
- High transaction velocity
- Very new account
- Synthetic high-risk geography marker

Each condition adds points to the transaction's risk score.

### Risk levels

| Score | Risk level |
|---:|---|
| 0-24 | Low |
| 25-49 | Medium |
| 50-74 | High |
| 75+ | Critical |

The exact thresholds and weights are stored in:

```text
config/risk_rules.json
```

That makes the rules easy to change without rewriting the scoring logic.

## Example output

The alert file contains fields such as:

```text
transaction_id
customer_id
timestamp
amount
country
risk_score
risk_level
risk_reasons
```

Example:

```text
TXN000123,CUST0042,2026-10-20 12:15:00,42000.00,Country-A,65,High,"High amount | High KYC risk | New payee"
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/risk-monitoring-python.git
cd risk-monitoring-python
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the project

### Step 1: Generate synthetic data

```bash
python -m src.generate_data
```

This creates:

```text
data/transactions.csv
```

### Step 2: Run risk monitoring

```bash
python -m src.main
```

This creates:

```text
outputs/scored_transactions.csv
outputs/risk_alerts.csv
outputs/risk_summary.csv
```

### Step 3: Run the dashboard

```bash
streamlit run dashboard.py
```

Streamlit will display a local URL, normally:

```text
http://localhost:8501
```

## Run tests

```bash
pytest
```

The GitHub Actions workflow also runs the tests automatically whenever code is pushed to GitHub.

## How the scoring works

The risk engine returns two important outputs:

1. `risk_score`
2. `risk_reasons`

For example:

```text
risk_score = 55
risk_reasons = "High transaction amount | Multiple failed logins | New payee"
```

This is useful because an analyst can see not only that a transaction was flagged, but also **why** it was flagged.

## Portfolio / interview explanation

You can explain the project like this:

> I built a Python-based transaction risk monitoring project using synthetic data. I created configurable risk rules for transaction amount, KYC risk, login behaviour, chargeback history, geographic anomalies, payee status, transaction velocity, and account age. The system calculates an explainable risk score, assigns a severity level, exports investigation alerts, and displays monitoring results in a Streamlit dashboard. I also added pytest tests and GitHub Actions for automated quality checks.

## Suggested GitHub repository description

```text
Python risk monitoring project using synthetic transaction data, configurable risk rules, explainable scoring, alert generation, Streamlit dashboard, pytest, and GitHub Actions.
```

## Suggested GitHub topics

```text
python
risk-monitoring
fraud-detection
transaction-monitoring
data-analysis
pandas
streamlit
risk-management
compliance
portfolio-project
```

## Possible future improvements

- Add SQL / SQLite storage
- Add Power BI export
- Add investigation case status
- Add customer-level risk aggregation
- Add alert deduplication
- Add machine-learning anomaly detection
- Add time-series trend monitoring
- Add email or Slack-style alert simulation
- Add REST API with FastAPI
- Add Docker support

## Disclaimer

This is an educational project using synthetic data. It should not be used as a real fraud, AML, KYC, financial-crime, credit-risk, or regulatory decisioning system without appropriate governance, validation, security, legal review, and domain-specific controls.

## License

MIT License
