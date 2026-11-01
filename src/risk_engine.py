import json
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RULES_FILE = PROJECT_ROOT / "config" / "risk_rules.json"


def load_rules(rules_file: Path = DEFAULT_RULES_FILE) -> dict[str, Any]:
    """Load risk-scoring rules from JSON."""
    with rules_file.open("r", encoding="utf-8") as file:
        return json.load(file)


def calculate_risk_score(
    row: pd.Series,
    rules: dict[str, Any],
) -> tuple[int, list[str]]:
    """
    Calculate a transparent rule-based risk score for one transaction.

    Returns:
        tuple:
            risk_score: integer score
            reasons: list of triggered risk rules
    """
    limits = rules["limits"]
    weights = rules["weights"]
    high_risk_countries = set(rules["synthetic_high_risk_countries"])

    score = 0
    reasons: list[str] = []

    if float(row["amount"]) >= limits["high_amount"]:
        score += weights["high_amount"]
        reasons.append("High transaction amount")

    if str(row["kyc_risk"]).lower() == "high":
        score += weights["high_kyc_risk"]
        reasons.append("High KYC risk")

    if int(row["failed_logins_24h"]) >= limits["failed_logins"]:
        score += weights["failed_logins"]
        reasons.append("Multiple failed logins")

    if int(row["chargeback_history"]) >= limits["chargeback_history"]:
        score += weights["chargeback_history"]
        reasons.append("Previous chargebacks")

    if float(row["ip_distance_km"]) >= limits["ip_distance_km"]:
        score += weights["large_ip_distance"]
        reasons.append("Large IP-location change")

    if int(row["is_new_payee"]) == 1:
        score += weights["new_payee"]
        reasons.append("New payee")

    if int(row["velocity_1h"]) >= limits["velocity_1h"]:
        score += weights["high_velocity_1h"]
        reasons.append("High 1-hour transaction velocity")

    if int(row["velocity_24h"]) >= limits["velocity_24h"]:
        score += weights["high_velocity_24h"]
        reasons.append("High 24-hour transaction velocity")

    if int(row["account_age_days"]) <= limits["new_account_days"]:
        score += weights["new_account"]
        reasons.append("New account")

    if str(row["country"]) in high_risk_countries:
        score += weights["synthetic_high_risk_country"]
        reasons.append("Synthetic high-risk geography marker")

    return score, reasons


def classify_risk(score: int, rules: dict[str, Any]) -> str:
    """Convert a numeric score into a risk level."""
    thresholds = rules["risk_thresholds"]

    if score >= thresholds["critical"]:
        return "Critical"
    if score >= thresholds["high"]:
        return "High"
    if score >= thresholds["medium"]:
        return "Medium"
    return "Low"


def score_dataframe(
    dataframe: pd.DataFrame,
    rules: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """Score all transactions and add explainable risk columns."""
    if rules is None:
        rules = load_rules()

    scored = dataframe.copy()

    results = scored.apply(
        lambda row: calculate_risk_score(row, rules),
        axis=1,
    )

    scored["risk_score"] = results.apply(lambda item: item[0])
    scored["risk_reasons"] = results.apply(
        lambda item: " | ".join(item[1]) if item[1] else "No major risk rules triggered"
    )
    scored["risk_level"] = scored["risk_score"].apply(
        lambda score: classify_risk(int(score), rules)
    )

    return scored
