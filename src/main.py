from pathlib import Path

import pandas as pd

from src.risk_engine import load_rules, score_dataframe


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "transactions.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def validate_input(dataframe: pd.DataFrame) -> None:
    """Basic data-quality validation before risk scoring."""
    required_columns = {
        "transaction_id",
        "customer_id",
        "timestamp",
        "amount",
        "country",
        "channel",
        "kyc_risk",
        "failed_logins_24h",
        "chargeback_history",
        "ip_distance_km",
        "is_new_payee",
        "velocity_1h",
        "velocity_24h",
        "account_age_days",
    }

    missing_columns = required_columns - set(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"Input data is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    if dataframe["transaction_id"].duplicated().any():
        raise ValueError("Duplicate transaction_id values detected.")

    if (dataframe["amount"] < 0).any():
        raise ValueError("Negative transaction amounts detected.")


def create_summary(scored: pd.DataFrame) -> pd.DataFrame:
    """Create a compact risk-monitoring summary."""
    summary = (
        scored.groupby("risk_level", as_index=False)
        .agg(
            transaction_count=("transaction_id", "count"),
            total_amount=("amount", "sum"),
            average_risk_score=("risk_score", "mean"),
        )
    )

    order = {
        "Low": 1,
        "Medium": 2,
        "High": 3,
        "Critical": 4,
    }

    summary["sort_order"] = summary["risk_level"].map(order)
    summary = summary.sort_values("sort_order").drop(columns="sort_order")
    summary["total_amount"] = summary["total_amount"].round(2)
    summary["average_risk_score"] = summary["average_risk_score"].round(2)

    return summary


def main() -> None:
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "Synthetic data file not found. "
            "Run `python -m src.generate_data` first."
        )

    dataframe = pd.read_csv(DATA_FILE)
    validate_input(dataframe)

    rules = load_rules()
    scored = score_dataframe(dataframe, rules)

    alert_levels = ["High", "Critical"]
    alerts = scored[scored["risk_level"].isin(alert_levels)].copy()

    summary = create_summary(scored)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    scored_file = OUTPUT_DIR / "scored_transactions.csv"
    alerts_file = OUTPUT_DIR / "risk_alerts.csv"
    summary_file = OUTPUT_DIR / "risk_summary.csv"

    scored.to_csv(scored_file, index=False)
    alerts.to_csv(alerts_file, index=False)
    summary.to_csv(summary_file, index=False)

    print("Risk monitoring completed.")
    print(f"Transactions scored: {len(scored):,}")
    print(f"High/Critical alerts: {len(alerts):,}")
    print()
    print(summary.to_string(index=False))
    print()
    print(f"Saved: {scored_file}")
    print(f"Saved: {alerts_file}")
    print(f"Saved: {summary_file}")


if __name__ == "__main__":
    main()
