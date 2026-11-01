import pandas as pd

from src.risk_engine import (
    calculate_risk_score,
    classify_risk,
    load_rules,
    score_dataframe,
)


def make_base_transaction() -> pd.Series:
    return pd.Series(
        {
            "amount": 1000,
            "country": "India",
            "channel": "Web",
            "kyc_risk": "Low",
            "failed_logins_24h": 0,
            "chargeback_history": 0,
            "ip_distance_km": 50,
            "is_new_payee": 0,
            "velocity_1h": 1,
            "velocity_24h": 3,
            "account_age_days": 500,
        }
    )


def test_low_risk_transaction_scores_zero() -> None:
    rules = load_rules()
    row = make_base_transaction()

    score, reasons = calculate_risk_score(row, rules)

    assert score == 0
    assert reasons == []


def test_high_amount_adds_expected_score() -> None:
    rules = load_rules()
    row = make_base_transaction()
    row["amount"] = 50000

    score, reasons = calculate_risk_score(row, rules)

    assert score == rules["weights"]["high_amount"]
    assert "High transaction amount" in reasons


def test_multiple_rules_create_high_risk_score() -> None:
    rules = load_rules()
    row = make_base_transaction()

    row["amount"] = 50000
    row["kyc_risk"] = "High"
    row["is_new_payee"] = 1

    score, reasons = calculate_risk_score(row, rules)

    assert score == 55
    assert classify_risk(score, rules) == "High"
    assert len(reasons) == 3


def test_score_dataframe_adds_expected_columns() -> None:
    dataframe = pd.DataFrame([make_base_transaction()])
    scored = score_dataframe(dataframe)

    assert "risk_score" in scored.columns
    assert "risk_level" in scored.columns
    assert "risk_reasons" in scored.columns
    assert scored.loc[0, "risk_level"] == "Low"
