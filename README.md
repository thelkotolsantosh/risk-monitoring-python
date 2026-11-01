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

---

## About the Project

Risk monitoring teams often review large volumes of transactions and customer activity to identify unusual behaviour that may require investigation.

This project demonstrates how Python can be used to build a simple, explainable transaction-monitoring system.

Instead of using real customer information, the application generates synthetic transactions and evaluates them using configurable risk rules.

The goal of the project is to demonstrate practical skills in:

- Python
- Data analysis
- Risk monitoring
- Transaction monitoring
- Fraud detection concepts
- Explainable risk scoring
- Alert generation
- Pandas
- NumPy
- Streamlit
- Automated testing
- GitHub Actions

---

## Project Workflow

```text
Synthetic Transaction Data
          |
          v
   Data Validation
          |
          v
   Risk Rule Engine
          |
          v
   Risk Score Calculation
          |
          v
 Risk Classification
          |
          v
 Alert Generation
          |
          v
 CSV Reports / Dashboard
