## Frequently Asked Questions

### 1. Why did you build this project?

I wanted to understand how transaction monitoring can be handled with Python using simple risk rules. The main goal was to create something practical that shows how a transaction can be reviewed, scored, and flagged.

### 2. Is the transaction data real?

No. All the data used in this project is synthetic. It does not contain customer information, bank data, or company data.

### 3. How is the risk score calculated?

Each transaction is checked against a set of rules. If a rule is triggered, a certain number of points are added to the score. The final score decides whether the transaction is Low, Medium, High, or Critical risk.

### 4. Why did you use rule-based scoring instead of machine learning?

I wanted the first version to be easy to understand. With rule-based scoring, I can clearly see why a transaction was flagged and adjust the rules without retraining a model.

### 5. Can I change the risk thresholds?

Yes. The thresholds and weights are stored in `config/risk_rules.json`, so they can be changed without editing most of the Python code.

### 6. What happens when a transaction is marked High or Critical?

High and Critical transactions are included in the alert output. They can then be reviewed separately as possible investigation cases.

### 7. What kind of risk signals are checked?

The current version checks things like transaction amount, KYC risk, failed logins, chargebacks, transaction frequency, new payees, account age, and changes in IP location.

### 8. Does this project detect actual fraud?

No. It only identifies transactions that match the configured risk rules. A flagged transaction is not automatically fraud.

### 9. Why are the reasons for the score included?

I wanted the alerts to be explainable. Instead of only showing a score like `65`, the system also shows which rules were triggered.

### 10. What does the Streamlit dashboard do?

The dashboard gives a quick view of the generated data and alerts. It shows transaction counts, risk levels, high-risk cases, and some basic breakdowns.

### 11. Do I need Streamlit to run the risk engine?

No. Streamlit is only used for the dashboard. The main risk-monitoring process can run from Python without opening the dashboard.

### 12. Why did you use Pandas?

Pandas makes it easier to load, filter, score, and export transaction data. It is also commonly used for this type of data analysis in Python.

### 13. What is stored in `risk_alerts.csv`?

That file contains the transactions classified as High or Critical risk, along with their scores and the reasons they were flagged.

### 14. What is the difference between `scored_transactions.csv` and `risk_alerts.csv`?

`scored_transactions.csv` contains every transaction. `risk_alerts.csv` contains only the transactions that reached the High or Critical risk level.

### 15. Why did you add tests?

The tests help confirm that the scoring logic behaves as expected. For example, they check that a high-value transaction receives the correct score.

### 16. What does GitHub Actions do in this project?

GitHub Actions automatically runs the tests when changes are pushed to the repository. It is a simple way to catch problems after code changes.

### 17. Can this project be connected to a database?

Yes. The current version uses CSV files to keep things simple, but it can be extended to use SQLite, PostgreSQL, SQL Server, or another database.

### 18. Can machine learning be added later?

Yes. A future version could compare the current rule-based score with an anomaly-detection or classification model.

### 19. Is this suitable for a real banking or AML system?

No. This is a learning project. Real financial monitoring systems need stronger controls, testing, audit trails, data governance, security, and regulatory review.

### 20. What would you improve next?

The next useful improvement would be adding case management so an alert can move through statuses such as New, Under Review, Escalated, False Positive, and Closed.
